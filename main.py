from fastapi import FastAPI, Depends
from api import api_router
from core import register_exception_handler
from core.async_redis import redis, global_rate_limit
from redis.exceptions import ConnectionError


app = FastAPI(
    dependencies=[
        Depends(global_rate_limit)
    ]
)

app.include_router(api_router)

register_exception_handler(app)


@app.on_event('startup')
async def startup():
    try:
        await redis.ping()
    except ConnectionError:
        print('Redis disconnected')


@app.on_event('shutdown')
async def shutdown():
    await redis.close()
    print('Redis closed')