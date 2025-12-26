from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException, status
from uuid import UUID
from numpy import array, float64, take, isnan, where, nanmean
from .enums import KmeansInit, Normalization


class PCAInit(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    n_components: int = Field(2, gt=0)
    random_state: int | None = 1


class KmeansScheme(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    n_clusters: int = Field(gt=0)
    max_iter: int = 100
    tol: float = Field(1e-4, gt=0, lt=1)
    init: KmeansInit = KmeansInit.kmeans_pp
    random_state: int | None = 1


class KmeansDataCreate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    kmeans: KmeansScheme
    normalization: Normalization | None = Normalization.z_score
    pca: PCAInit | None
    description: str | None = None
    chat_id: UUID


class KmeansDataUpdateFull(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    kmeans: KmeansScheme
    normalization: Normalization | None
    pca: PCAInit | None
    description: str


class KmeansDataUpdatePartial(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    kmeans: KmeansScheme | None = None
    normalization: Normalization | None = None
    pca: PCAInit | None = None
    description: str | None = None


class KmeansDataRead(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    n_clusters: int
    preprocessing: dict
    description: str | None = None


class KmeansDataDBCreate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    n_cluster: int
    preprocessing: dict
    description: str | None = None
    chat_id: UUID


class KmeansDataDBUpdateFull(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    n_cluster: int
    preprocessing: dict
    description: str
    chat_id: UUID


class KmeansDataDBUpdatePartial(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    n_cluster: int | None = None
    preprocessing: dict | None = None
    description: str | None = None
    chat_id: UUID | None = None


class KmeansCentroidCreate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    values: list[list[float]]
    fit_time: float
    kmeans_data_id: UUID


class KmeansCentroidRead(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    values: list[list[float]]
    fit_at: datetime
    fit_time: float
    kmeans_data: KmeansDataRead


class KmeansFit(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    X: list[list[float | None]]
    kmeans_data_id: UUID


    @field_validator('X')
    def verify_X(cls, value):
        X = array(value, dtype=float64)
        if X.ndim != 2:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='X must be 2D matrix'
            )
        col_mean = nanmean(X, axis=0)
        ind = where(isnan(X))
        X[ind] = take(col_mean, ind[1])
        return X