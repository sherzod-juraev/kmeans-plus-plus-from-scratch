from typing import Annotated
from time import perf_counter
from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from numpy import ndarray
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from database import get_db
from database.session import Async_Session_Local
from kmeans import Kmeans
from . import (
    crud,
    KmeansDataCreate,
    KmeansDataDBCreate,
    KmeansCentroidCreate,
    KmeansFit,
    KmeansCentroidRead,
    KmeansDataRead
)
from core.async_redis import rate_limit


kmeans_router = APIRouter(
    dependencies=[
        Depends(rate_limit)
    ]
)


async def kmeans_fit_background(
        kmeans_data_scheme: KmeansDataCreate,
        X: ndarray
):
    async with Async_Session_Local() as db:
        kmeans = Kmeans()
        try:
            kmeans_data_db_scheme = KmeansDataDBCreate(
                n_clusters=kmeans_data_scheme.kmeans.n_clusters,
                preprocessing={
                    'normalization': kmeans_data_scheme.normalization,
                    'pca': 'False' if kmeans_data_scheme.pca is None else 'True'
                },
                description=kmeans_data_scheme.description,
                chat_id=kmeans_data_scheme.chat_id
            )
            kmeans_data_model = await crud.create_kmeans_data(db, kmeans_data_db_scheme)
            if kmeans_data_scheme.normalization:
                if kmeans_data_scheme.normalization == 'z_score':
                    X = StandardScaler().fit_transform(X)
                else:
                    X = MinMaxScaler().fit_transform(X)
            if kmeans_data_scheme.pca:
                X = PCA(
                    n_components=kmeans_data_scheme.pca.n_components,
                    random_state=kmeans_data_scheme.pca.random_state
                ).fit_transform(X)
            for field, value in kmeans_data_scheme.kmeans.model_dump().items():
                setattr(kmeans, field, value)
            start_time = perf_counter()
            centroids = kmeans.fit(X).centroids.tolist()
            kmeans_centroid_scheme = KmeansCentroidCreate(
                values=centroids,
                fit_time=perf_counter() - start_time,
                kmeans_data_id=kmeans_data_model.id
            )
            await crud.create_kmeans_centroid(db, kmeans_centroid_scheme)
        except Exception as exc:
            await db.rollback()
            raise exc
        finally:
            await db.close()

@kmeans_router.post(
    '/fit',
    summary='Kmeans fit and create kmeans_data',
    status_code=status.HTTP_200_OK
)
async def fit_kmeans(
        kmeans_data_scheme: KmeansDataCreate,
        kmeans_fit_scheme: KmeansFit,
        background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        kmeans_fit_background,
        kmeans_data_scheme,
        kmeans_fit_scheme.X
    )
    return {'status': 'Fit started'}


@kmeans_router.delete(
    '/{kmeans_data_id}',
    summary='Delete kmeans_data',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_kmeans_data(
        kmeans_data_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    await crud.delete_kmeans_data(db, kmeans_data_id)


@kmeans_router.get(
    '/{kmeans_data_id}',
    summary='Get kmeans centroids with kmeans_data by kmeans_data_id',
    status_code=status.HTTP_200_OK,
    response_model=list[KmeansCentroidRead]
)
async def get_kmeans_centroids(
        kmeans_data_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)],
        skip: int = 0,
        limit: int = 10
):
    kmeans_centroids_list = await crud.read_kmeans_centroids(db, kmeans_data_id, skip, limit)
    return kmeans_centroids_list


@kmeans_router.get(
    '/',
    summary='Get kmeans datas',
    status_code=status.HTTP_200_OK,
    response_model=list[KmeansDataRead]
)
async def get_kmeans_datas(
        db: Annotated[AsyncSession, Depends(get_db)],
        skip: int = 0,
        limit: int = 10
):
    kmeans_datas_list = await crud.read_kmeans_datas(db, skip, limit)
    return kmeans_datas_list