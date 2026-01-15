from redis.asyncio import Redis
from core import get_setting


settings = get_setting()
redis = Redis.from_url(
    url=settings.redis_url,
    encoding='utf-8',
    decode_responses=True,
    health_check_interval=30
)