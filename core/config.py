from pydantic_settings import BaseSettings


class Setting(BaseSettings):

    database_url: str
    access_token_minutes: int
    refresh_token_days: int
    secret_key: str
    algorithm: str

    class Config:
        env_file = '.env'
        env_file_encoding='utf-8'


setting = Setting()