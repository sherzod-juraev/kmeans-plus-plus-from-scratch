from pydantic_settings import BaseSettings
from functools import lru_cache


class Setting(BaseSettings):

    database_url: str
    access_token_minutes: int
    refresh_token_days: int
    secret_key: str
    algorithm: str
    redis_url: str
    rate_limit: int
    rate_period: int
    global_rate_limit: int
    global_rate_period: int

    class Config:
        env_file = '.env'
        env_file_encoding='utf-8'


@lru_cache
def get_setting() -> Setting:
    settings = Setting()
    return settings