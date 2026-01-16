from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from . import User, UserCreate, UserUpdateFull, \
    UserUpdatePartial, UserDelete
from core import hashed_pass, verify_pass


async def save_to_db(
        db: AsyncSession,
        user_model: User,
        /
) -> User:
    try:
        await db.commit()
        await db.refresh(user_model)
        return user_model
    except IntegrityError as exc:
        await db.rollback()
        err_msg = str(exc.orig)
        if 'ix_users_username' in err_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username already exists'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating user'
        )


async def create_user(
        db: AsyncSession,
        user_scheme: UserCreate,
        /
) -> User:
    user_model = User(
        username=user_scheme.username,
        password=hashed_pass(user_scheme.password)
    )
    db.add(user_model)
    user_model = await save_to_db(db, user_model)
    return user_model


async def user_read(
        db: AsyncSession,
        user_id: UUID,
        /
) -> User:
    user_model = await db.get(User, user_id)
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user_model


async def update_user(
        db: AsyncSession,
        user_id: UUID,
        user_scheme: UserUpdateFull | UserUpdatePartial,
        /, *,
        exclude_unset: bool = False
) -> User:
    user_model = await user_read(db, user_id)
    for field, value in user_scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(user_model, field, value)
    user_model = await save_to_db(db, user_model)
    return user_model


async def delete_user(
        db: AsyncSession,
        user_id: UUID,
        /
) -> None:
    user_model = await user_read(db, user_id)
    await db.delete(user_model)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error deleting user'
        )