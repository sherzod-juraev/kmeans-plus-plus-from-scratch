from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from core import get_setting

settings = get_setting()


async_engine = create_async_engine(
    url=settings.database_url,
    pool_size=40,
    max_overflow=60,
    pool_recycle=1800,
    pool_timeout=3
)


Async_Session_Local = async_sessionmaker(bind=async_engine)
Base = declarative_base()