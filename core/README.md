# Core Package

The `core/` package provides essential
configurations, security utilities, and
exception handling for the FastAPI project.
It centralizes settings, token management,
password hashing, and custom exception handlers.

## Table of Contents

- [File descriptions](#file-descriptions)
  - [__init__.py](#__init__py)
  - [config.py](#configpy)
  - [exception.py](#exceptionpy)
  - [security.py](#securitypy)
- [Usage examples](#usage-examples)
  - [Dependency Injection for FastAPI routes](#dependency-injection-for-fastapi-routes)
  - [Password hashing](#password-hashing)
  - [Creating tokens](#creating-tokens)

## File Descriptions

### `__init__.py`
- Exposes `setting`, `register_exception_handler`,
- and security functions for use in other modules.

### `config.py`
- Uses `Pydantic BaseSettings` to load application 
settings from `.env`.
- Example settings:
  - `database_url`
  - `access_token_minutes`
  - `refresh_token_days`
  - `secret_key`
  - `algorithm`
- Enables easy configuration management and type validation.

### `exception.py`
- Registers FastAPI exception handlers for:
  - `TimeoutError` → HTTP 503
  - `ResponseValidationError` → HTTP 503
  - `RequestValidationError` → HTTP 400
- Returns JSON responses with appropriate `status_code` and `detail`.

### `security.py`
- Provides secure password hashing and verification using `passlib` (bcrypt).
- JWT token creation and verification:
  - `create_access_token` and `verify_access_token`
  - `create_refresh_token` and `verify_refresh_token`
- Integrates with FastAPI's `OAuth2PasswordBearer` for authentication dependencies.
- Raises proper HTTP exceptions for invalid or expired tokens.

## Usage Examples

### Dependency Injection for FastAPI routes
```python
from core import verify_access_token
from uuid import UUID
from fastapi import Depends

async def protected_route(user_id: UUID = Depends(verify_access_token)):
    return {"user_id": user_id}
```

### Password hashing

```python
from core import hashed_pass, verify_pass

hashed = hashed_pass("my_secure_password")
assert verify_pass("my_secure_password", hashed)
```

### Creating Tokens

```python
from core import create_access_token, create_refresh_token
from uuid import uuid4

user_id = uuid4()

access_token = create_access_token(user_id)
refresh_token = create_refresh_token(user_id)
```

## Important Notes

- All sensitive settings are stored in the
.env file and accessed via core.config.setting.
- Tokens follow JWT standards and include expiration times.
- Exception handlers ensure consistent API error responses across the project.