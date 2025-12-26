from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException, status
from uuid import UUID
from . import KmeansData, KmeansCentroid, \
    KmeansDataDBCreate, KmeansCentroidCreate


async def persist_kmeans_data(
        db: AsyncSession,
        kmeans_data_model: KmeansData,
        /
) -> KmeansData:
    try:
        await db.flush()
        await db.refresh(kmeans_data_model)
        return kmeans_data_model
    except IntegrityError as exc:
        await db.rollback()
        err_msg = str(exc.orig)
        if 'kmeans_data_chat_id_fkey' in err_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Chat not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating kmeans_data'
        )


async def persist_kmeans_centroid(
        db: AsyncSession,
        kmeans_centroid_model: KmeansCentroid,
        /
) -> KmeansCentroid:
    try:
        await db.flush()
        await db.refresh(kmeans_centroid_model)
        return kmeans_centroid_model
    except IntegrityError as exc:
        await db.rollback()
        err_msg = str(exc.orig)
        if 'kmeans_centroids_kmeans_data_id_fkey' in err_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Kmeans_data not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating kmeans_centroid'
        )


async def save_kmeans_data(
        db: AsyncSession,
        kmeans_data_model: KmeansData,
        /
) -> KmeansData:
    try:
        await db.commit()
        await db.refresh(kmeans_data_model)
        return kmeans_data_model
    except IntegrityError as exc:
        await db.rollback()
        err_msg = str(exc.orig)
        if 'kmeans_data_chat_id_fkey' in err_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Chat not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating kmeans_data'
        )


async def save_kmeans_centroid(
        db: AsyncSession,
        kmeans_centroid_model: KmeansCentroid,
        /
) -> KmeansCentroid:
    try:
        await db.commit()
        await db.refresh(kmeans_centroid_model)
        return kmeans_centroid_model
    except IntegrityError as exc:
        await db.rollback()
        err_msg = str(exc.orig)
        if 'kmeans_centroids_kmeans_data_id_fkey' in err_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Kmeans_data not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating kmeans_centroid'
        )


async def create_kmeans_data(
        db: AsyncSession,
        kmeans_data_scheme: KmeansDataDBCreate,
        /
) -> KmeansData:
    kmeans_data_model = KmeansData(
        n_clusters=kmeans_data_scheme.n_clusters,
        preprocessing=kmeans_data_scheme.preprocessing,
        description=kmeans_data_scheme.description,
        chat_id=kmeans_data_scheme.chat_id
    )
    db.add(kmeans_data_model)
    kmeans_data_model = await persist_kmeans_data(db, kmeans_data_model)
    return kmeans_data_model


async def create_kmeans_centroid(
        db: AsyncSession,
        kmeans_centroid_scheme: KmeansCentroidCreate,
        /
) -> KmeansCentroid:
    kmeans_centroid_model = KmeansCentroid(
        values=kmeans_centroid_scheme.values,
        fit_time=kmeans_centroid_scheme.fit_time,
        kmeans_data_id=kmeans_centroid_scheme.kmeans_data_id
    )
    db.add(kmeans_centroid_model)
    kmeans_centroid_model = await persist_kmeans_centroid(db, kmeans_centroid_model)
    kmeans_centroid_model = await save_kmeans_centroid(db, kmeans_centroid_model)
    return kmeans_centroid_model


async def read_kmeans_data(
        db: AsyncSession,
        kmeans_data_id: UUID,
        /
) -> KmeansData:
    kmeans_data_model = await db.get(KmeansData, kmeans_data_id)
    if kmeans_data_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Kmeans_data not found'
        )
    return kmeans_data_model


async def read_kmeans_centroids(
        db: AsyncSession,
        kmeans_data_id: UUID,
        skip: int, limit: int,
        /
) -> list[KmeansCentroid]:
    query = select(KmeansCentroid).where(
        KmeansCentroid.kmeans_data_id == kmeans_data_id
    ).order_by(KmeansCentroid.fit_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    kmeans_centroid_list = result.scalars().all()
    return kmeans_centroid_list


async def delete_kmeans_data(
        db: AsyncSession,
        kmeans_data_id: UUID,
        /
) -> None:
    kmeans_data_model = await read_kmeans_data(db, kmeans_data_id)
    await db.delete(kmeans_data_model)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error deleting kmeans_data'
        )