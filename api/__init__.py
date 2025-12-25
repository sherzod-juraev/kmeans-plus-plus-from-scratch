from fastapi import APIRouter


# import routers
from .users.router import user_router


# import models
from .users import User


__all__ = ['User']


api_router = APIRouter()


api_router.include_router(
    user_router,
    prefix='/auth',
    tags=['Authenticate']
)