from fastapi import APIRouter, status
from .scheme import KmeansOptions, DataUploadJSON


api_router = APIRouter()


@api_router.post(
    '/set-options',
    summary='Set kmeans settings',
    status_code=status.HTTP_200_OK,
    response_model=bool
)
async def set_options(
        kmeans_settings: KmeansOptions
) -> bool:
    pass


@api_router.post(
    '/data-upload-json',
    summary='Load json data for kmeans',
    status_code=status.HTTP_200_OK,
    response_model=str
)
async def data_upload_json(
        data: DataUploadJSON
):
    pass