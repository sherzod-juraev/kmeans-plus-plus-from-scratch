from fastapi import FastAPI, Depends
from api import api_router
from core import register_exception_handler, get_logger, log_request_middleware
from core.async_redis import redis, global_rate_limit
from redis.exceptions import ConnectionError


app = FastAPI(
    dependencies=[
        Depends(global_rate_limit)
    ]
)

app.include_router(api_router)
app.middleware('http')(log_request_middleware)
register_exception_handler(app)

logger = get_logger('kmeans')


@app.on_event('startup')
async def startup():
    logger.info('Server started')
    try:
        await redis.ping()
        logger.info('Redis connected')
    except ConnectionError as ex:
        logger.error(f'Redis disconnected | Server unavailable | RedisConnectionError {ex}')
        raise ex


@app.on_event('shutdown')
async def shutdown():
    await redis.close()
    logger.critical('Server shutdown detected | Redis closed')