from fastapi import FastAPI
from api import api_router
from core import register_exception_handler


app = FastAPI()

app.include_router(api_router)

register_exception_handler(app)