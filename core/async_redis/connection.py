from redis.asyncio import Redis
from core import get_setting


settings = get_setting()
redis = Redis.from_url(url=settings.redis_url)