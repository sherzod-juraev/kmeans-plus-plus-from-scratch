from typing import Annotated
from fastapi import APIRouter, Depends, status
from uuid import UUID
from core import verify_access_token as vat
from database import get_db
from . import crud, ChatCreate, ChatUpdateFull, \
    ChatUpdatePartial, ChatRead
from core.async_redis import rate_limit


chat_router = APIRouter(
    dependencies=[
        Depends(rate_limit)
    ]
)


@chat_router.post(
    '/',
    summary='Create chat',
    status_code=status.HTTP_201_CREATED,
    response_model=ChatRead
)
async def create_chat(
        user_id: Annotated[UUID, Depends(vat)],
        chat_scheme: ChatCreate,
        db=Depends(get_db)
):
    chat_model = await crud.create_chat(db, user_id, chat_scheme)
    return chat_model


@chat_router.put(
    '/{chat_id}',
    summary='Full update chat',
    status_code=status.HTTP_200_OK,
    response_model=ChatRead,
    dependencies=[Depends(vat)]
)
async def full_update_chat(
        chat_id: UUID,
        chat_scheme: ChatUpdateFull,
        db=Depends(get_db)
):
    chat_model = await crud.update_chat(db, chat_id, chat_scheme)
    return chat_model


@chat_router.patch(
    '/{chat_id}',
    summary='Partial update chat',
    status_code=status.HTTP_200_OK,
    response_model=ChatRead,
    dependencies=[Depends(vat)]
)
async def partial_update_chat(
        chat_id: UUID,
        chat_scheme: ChatUpdatePartial,
        db=Depends(get_db)
):
    chat_model = await crud.update_chat(db, chat_id, chat_scheme, exclude_unset=True)
    return chat_model


@chat_router.delete(
    '/{chat_id}',
    summary='Delete chat',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(vat)]
)
async def delete_chat(
        chat_id: UUID,
        db=Depends(get_db)
):
    await crud.delete_chat(db, chat_id)


@chat_router.get(
    '/{chat_id}',
    summary='Get chat',
    status_code=status.HTTP_200_OK,
    response_model=ChatRead,
    dependencies=[Depends(vat)]
)
async def get_chat(
        chat_id: UUID,
        db=Depends(get_db)
):
    chat_model = await crud.read_chat(db, chat_id)
    return chat_model


@chat_router.get(
    '/',
    summary='Get chats list',
    status_code=status.HTTP_200_OK,
    response_model=list[ChatRead]
)
async def get_chats_list(
        user_id: Annotated[UUID, Depends(vat)],
        skip: int = 0,
        limit: int = 10,
        db=Depends(get_db)
):
    chats = await crud.get_chats(db, user_id, skip, limit)
    return chats