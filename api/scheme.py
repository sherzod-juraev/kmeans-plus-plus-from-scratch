from pydantic import BaseModel, field_validator
from fastapi import HTTPException, status
import numpy as np


class KmeansOptions(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    n_clusters: int = 3
    max_iter: int = 100


    @field_validator('n_clusters')
    def verify_n_clusters(cls, value):
        if value < 2:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='n_cluster must be 2 or greater'
            )
        return value


    @field_validator('max_iter')
    def verify_max_iter(cls, value):
        if value <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='max_iter cannot be < 0. Enter a positive integer for max_iter.'
            )
        return value


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