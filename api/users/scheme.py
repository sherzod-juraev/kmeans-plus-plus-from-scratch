from re import match
from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator, Field
from uuid import UUID


def validate_username(value: str, /) -> str:
    pattern = r'^[a-z0-9_-]{3,50}$'
    if not match(pattern, value):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Username invalid'
        )
    return value


def validate_password(value: str, /) -> str:
    pattern = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,25}$'
    if not match(pattern, value):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Password invalid'
        )
    return value


def validate_full_name(value: str, /) -> str:
    pattern = r'^[A-Za-z -]{1,100}$'
    if not match(pattern, value):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Full name invalid'
        )
    return value


class UserCreate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    username: str
    password: str


    @field_validator('username')
    def verify_username(cls, value):
        return validate_username(value)


    @field_validator('password')
    def verify_password(cls, value):
        return validate_password(value)


class UserUpdateFull(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    username: str
    full_name: str


    @field_validator('username')
    def verify_username(cls, value):
        return validate_username(value)


    @field_validator('full_name')
    def verify_full_name(cls, value):
        return validate_full_name(value)


class UserUpdatePartial(BaseModel):
    model_config = {
        'extra': 'forbid'
    }


    username: str | None = None
    full_name: str | None = None


    @field_validator('username')
    def verify_username(cls, value):
        if value is None:
            return value
        return validate_username(value)


    @field_validator('full_name')
    def verify_full_name(cls, value):
        if value is None:
            return value
        return validate_full_name(value)


class UserRead(BaseModel):
    model_config = {
        'from_attributes': True
    }


    id: UUID
    username: str
    full_name: str | None = None


class UserDelete(BaseModel):
    model_config = {
        'extra': 'forbid'
    }


    username: str
    password: str


    @field_validator('username')
    def verify_username(cls, value):
        return validate_username(value)


    @field_validator('password')
    def verify_password(cls, value):
        return validate_password(value)


class TokenResponse(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    access_token: str
    token_type: str = 'bearer'