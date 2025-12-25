from fastapi import APIRouter


# import routers


# import models
from .users import User


__all__ = ['User']


api_router = APIRouter()