from sqlalchemy.ext.asyncio import AsyncSession
from .connection import Async_Session_Local


async def get_db() -> AsyncSession:

    async with Async_Session_Local() as session:
        try:
            yield session
        except Exception as exc:
            await session.rollback()
            raise exc
        finally:
            await session.close()