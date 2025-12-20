from pydantic import BaseModel, field_validator, Field
from fastapi import HTTPException, status
from kmeans.options import NormalizationOptions, KmeansInitOptions
import numpy as np


class KmeansOptions(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    n_clusters: int = Field(2, ge=2)
    max_iter: int = Field(100, ge=0)
    tol: float = Field(1e-4, ge=0, lt=1e-1)
    init: KmeansInitOptions = KmeansInitOptions.KMEANS_PP
    random_state: int | None = None
    pca_n_components: int = Field(2, ge=2)
    normalization: NormalizationOptions = NormalizationOptions.Z_SCORE


class DataUploadJSON(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    X: list[list[float | None]]


    @field_validator('X')
    def verify_X(cls, value):
        value = np.array(value, dtype=np.float64)
        if value.ndim != 2:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='X must be a 2D matrix'
            )
        col_mean = np.mean(value, axis=0)
        indx = np.where(np.isnan(value))
        value[indx] = np.take(col_mean, indx[1])
        return value