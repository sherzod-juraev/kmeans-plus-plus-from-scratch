from pydantic_settings import BaseSettings
from functools import lru_cache


class Setting(BaseSettings):

    database_url: str
    access_token_minutes: int
    refresh_token_days: int
    secret_key: str
    algorithm: str
    redis_url: str
    rl_key: str
    rate_limit: int
    rate_period: int
    g_key: str
    gr_limit: int
    gr_period: int
    cb_key: str
    cb_limit: int
    cb_period: int

    class Config:
        env_file = '.env'
        env_file_encoding='utf-8'


@lru_cache
def get_setting() -> Setting:
    settings = Setting()
    return settings