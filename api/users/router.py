from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from uuid import UUID
from database import get_db
from core import create_refresh_token as crt, \
    create_access_token as cat, get_setting, \
    verify_refresh_token as vrt, verify_access_token as vat
from . import crud, UserCreate, UserRead, \
    UserUpdateFull, UserUpdatePartial, UserDelete, \
    TokenResponse
from core.async_redis import rate_limit


user_router = APIRouter(
    dependencies=[
        Depends(rate_limit)
    ]
)
settings = get_setting()


@user_router.post(
    '/signup',
    summary='Create a user',
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse
)
async def create_user(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db=Depends(get_db)
):
    user_scheme = UserCreate(
        username=form_data.username,
        password=form_data.password
    )
    user_model = await crud.create_user(db, user_scheme)
    response.set_cookie(
        key='refresh_token',
        value=crt(user_model.id),
        max_age=60 * 60 * 24 * settings.refresh_token_days,
        expires=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_days),
        httponly=True
    )
    token = TokenResponse(
        access_token=cat(user_model.id)
    )
    return token


@user_router.post(
    '/refresh',
    summary='Update access_token and refresh_token by refresh_token',
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse
)
async def update_access_token(
        request: Request,
        response: Response
):
    refresh_token = request.cookies.get('refresh_token')
    user_id = vrt(refresh_token)
    response.set_cookie(
        key='refresh_token',
        value=crt(user_id),
        max_age=60 * 60 * 24 * settings.refresh_token_days,
        expires=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_days),
        httponly=True
    )
    token = TokenResponse(
        access_token=cat(user_id)
    )
    return token


@user_router.put(
    '/',
    summary='Full update user',
    status_code=status.HTTP_200_OK,
    response_model=UserRead
)
async def update_full_user(
        user_id: Annotated[UUID, Depends(vat)],
        user_scheme: UserUpdateFull,
        db=Depends(get_db)
):
    user_model = await crud.update_user(db, user_id, user_scheme)
    return user_model


@user_router.patch(
    '/',
    summary='Partial update user',
    status_code=status.HTTP_200_OK,
    response_model=UserRead
)
async def partial_update_user(
        user_id: Annotated[UUID, Depends(vat)],
        user_scheme: UserUpdatePartial,
        db=Depends(get_db)
):
    user_model = await crud.update_user(db, user_id, user_scheme, exclude_unset=True)
    return user_model


@user_router.delete(
    '/',
    summary='Delete user',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
        response: Response,
        user_id: Annotated[UUID, Depends(vat)],
        db=Depends(get_db)
):
    await crud.delete_user(db, user_id)
    response.delete_cookie('refresh_token')


@user_router.get(
    '/',
    summary='Get user',
    status_code=status.HTTP_200_OK,
    response_model=UserRead
)
async def get_user(
        user_id: Annotated[UUID, Depends(vat)],
        db=Depends(get_db)
):
    user_model = await crud.user_read(db, user_id)
    return user_model