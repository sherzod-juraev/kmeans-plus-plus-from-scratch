from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException, status
from uuid import UUID
from . import Chat, ChatCreate, ChatUpdateFull, ChatUpdatePartial


async def save_to_db(
        db: AsyncSession,
        chat_model: Chat,
        /
) -> Chat:
    try:
        await db.commit()
        await db.refresh(chat_model)
        return chat_model
    except IntegrityError as exc:
        await db.rollback()
        err_msg = str(exc.orig)
        if 'chats_user_id_fkey' in err_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating chat'
        )


async def create_chat(
        db: AsyncSession,
        user_id: UUID,
        chat_scheme: ChatCreate,
        /
) -> Chat:
    chat_model = Chat(
        title=chat_scheme.title,
        description=chat_scheme.description,
        user_id=user_id
    )
    db.add(chat_model)
    chat_model = await save_to_db(db, chat_model)
    return chat_model


async def read_chat(
        db: AsyncSession,
        chat_id: UUID,
        /
) -> Chat:
    chat_model = await db.get(Chat, chat_id)
    if chat_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chat not found'
        )
    return chat_model


async def get_chats(
        db: AsyncSession,
        user_id: UUID,
        skip: int, limit: int,
        /
) -> list[Chat]:
    query = select(
        Chat).where(
        Chat.user_id == user_id).order_by(
        Chat.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    chats = result.scalars().all()
    if len(chats) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chat not found'
        )
    return chats


async def update_chat(
        db: AsyncSession,
        chat_id: UUID,
        chat_scheme: ChatUpdateFull | ChatUpdatePartial,
        /, *,
        exclude_unset: bool = False
) -> Chat:
    chat_model = await read_chat(db, chat_id)
    for field, value in chat_scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(chat_model, field, value)
    chat_model = await save_to_db(db, chat_model)
    return chat_model


async def delete_chat(
        db: AsyncSession,
        chat_id: UUID,
        /
) -> None:
    chat_model = await read_chat(db, chat_id)
    await db.delete(chat_model)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error deleting chat'
        )