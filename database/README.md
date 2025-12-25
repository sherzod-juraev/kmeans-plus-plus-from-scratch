# Database Package

The `database/` package provides
asynchronous SQLAlchemy sessions
for the FastAPI project. It handles
database connections and session
management for all CRUD and ORM
operations.

## File Descriptions

### `__init__.py`
- Exposes `Base` and `get_db` for use in other packages.

### `connection.py`
- Creates an asynchronous SQLAlchemy engine using `create_async_engine`.
- Configures connection pool parameters (`pool_size`, `max_overflow`, `pool_recycle`, `pool_timeout`) for performance.
- Provides `Base` via `declarative_base()` as a foundation for ORM models.

### `session.py`
- Provides the `get_db` dependency for FastAPI routes.
- Automatically handles session rollback on exceptions and ensures session closure.

## Usage
```python
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def some_endpoint(db: AsyncSession = Depends(get_db)):
    # Perform CRUD operations using db
    ...
```

## Important Notes

- `setting.database_url` is loaded from the `.env` file.
- Sessions are asynchronous and created per request.
- Automatic `rollback` and `close` ensures clean session management in case of errors.