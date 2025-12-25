from typing import Annotated
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from passlib.context import CryptContext
from core import setting


context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/signup')


# password hashed
def hashed_pass(raw_password: str, /) -> str:
    return context.hash(raw_password)

def verify_pass(raw_password: str, hashed_password: str, /) -> bool:
    return context.verify(raw_password, hashed_password)


# tokens
def create_access_token(auth_id: UUID, /) -> str:
    token_dict = {
        'sub': str(auth_id),
        'exp': datetime.utcnow() + timedelta(minutes=setting.access_token_minutes)
    }
    access_token = jwt.encode(token_dict, setting.secret_key, algorithm=setting.algorithm)
    return access_token


def create_refresh_token(auth_id: UUID, /) -> str:
    token_dict = {
        'sub': str(auth_id),
        'exp': datetime.utcnow() + timedelta(days=setting.refresh_token_days)
    }
    refresh_token = jwt.encode(token_dict, setting.secret_key, algorithm=setting.algorithm)
    return refresh_token


def verify_access_token(access_token: Annotated[str, Depends(oauth2_scheme)]) -> UUID:
    try:
        payload = jwt.decode(access_token, setting.secret_key, algorithms=[setting.algorithm])
        auth_id = payload.get('sub')
        if not auth_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='auth_id not found from access_token'
            )
        return UUID(auth_id)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expired',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token invalid',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )


def verify_refresh_token(refresh_token: str | None, /) -> UUID:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='refresh_token not found'
        )
    try:
        payload = jwt.decode(refresh_token, setting.secret_key, algorithms=[setting.algorithm])
        auth_id = payload.get('sub')
        if not auth_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='auth_id not found from refresh_token'
            )
        return UUID(auth_id)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='refresh_token expired'
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='refresh_token invalid'
        )