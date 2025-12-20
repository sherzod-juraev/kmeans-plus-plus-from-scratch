from fastapi import APIRouter, status
from .scheme import KmeansOptions, DataUploadJSON
from kmeans import Kmeans


api_router = APIRouter()

kmeans_model = Kmeans()


@api_router.post(
    '/set-options',
    summary='Set kmeans settings',
    status_code=status.HTTP_200_OK,
    response_model=None
)
async def set_options(
        kmeans_settings: KmeansOptions
):
    kmeans_model.n_clusters = kmeans_settings.n_clusters
    kmeans_model.max_iter = kmeans_settings.max_iter
    kmeans_model.tol = kmeans_settings.tol
    kmeans_model.init = kmeans_settings.init
    kmeans_model.random_state = kmeans_settings.random_state
    kmeans_model.pca_n_components = kmeans_settings.pca_n_components
    kmeans_model.normalization = kmeans_settings.normalization


@api_router.post(
    '/data-upload-json',
    summary='Load json data for kmeans',
    status_code=status.HTTP_200_OK,
    response_model=None
)
async def data_upload_json(
        data: DataUploadJSON
):
    kmeans_model.fit(data.X)

