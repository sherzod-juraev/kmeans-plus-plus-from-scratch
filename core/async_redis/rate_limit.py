from .connection import redis
from fastapi import Request, HTTPException, status
from core import get_setting


settings = get_setting()


async def get_ip(request: Request, /) -> str:

    forwarded = request.headers.get('X-Forwarded-For')
    client_ip = forwarded.split(',')[0] if forwarded else request.client.host
    return client_ip


async def get_urlpath(request: Request, /) -> str:
    url_path = request.scope['route'].path
    return url_path


async def rate_limit_helper(
        key: str,
        rate_limit: int,
        rate_period: int,
        /
) -> None:
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, rate_period)
    elif current > rate_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail='Too many requests'
        )


async def global_rate_limit(request: Request):
    client_ip = await get_ip(request)
    key = f'{settings.g_key}:{client_ip}'
    await rate_limit_helper(key, settings.gr_limit, settings.gr_period)


async def rate_limit(request: Request):
    client_ip = await get_ip(request)
    url_path = await get_urlpath(request)
    key = f'{settings.rl_key}:{url_path}:{client_ip}'
    await rate_limit_helper(key, settings.rate_limit, settings.rate_period)