from fastapi import APIRouter, Depends
from core import verify_access_token as vat


# import routers
from .users.router import user_router
from .chats.router import chat_router
from .kmeans.router import kmeans_router


# import models
from .users import User
from .chats import Chat
from .kmeans import KmeansData, KmeansCentroid


__all__ = [
    'User',
    'Chat',
    'KmeansData',
    'KmeansCentroid'
]


api_router = APIRouter()


api_router.include_router(
    user_router,
    prefix='/auth',
    tags=['Authenticate']
)


api_router.include_router(
    chat_router,
    prefix='/chat',
    tags=['Chats']
)


api_router.include_router(
    kmeans_router,
    prefix='/kmeans',
    tags=['Kmeans'],
    dependencies=[Depends(vat)]
)