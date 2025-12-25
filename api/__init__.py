from fastapi import APIRouter


# import routers
from .users.router import user_router
from .chats.router import chat_router


# import models
from .users import User
from .chats import Chat


__all__ = [
    'User',
    'Chat'
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