from .connection import redis
from fastapi import Request, HTTPException, status
from core import get_setting


settings = get_setting()


async def circuit_breaker(request: Request):
    key = f"{settings.cb_key}:route:{request.scope['route'].path}"
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, settings.cb_period)
    elif current > settings.cb_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail='Too many requests'
        )