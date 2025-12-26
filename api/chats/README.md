# Chat API

This package provides functionality to
manage `Chat` resources in a FastAPI
application. It includes database models,
CRUD operations, Pydantic schemas, and API
routes for creating, reading, updating, and
deleting chats.

## Table of Contents

- [Database Model](#database-model)
- [Schemas](#schemas)
- [CRUD Functions](#crud-functions)
- [API Routes](#api-routes)
- [Authentication](#authentication)

## Database Model

The `Chat` model represents a chat
belonging to a user.

```python
class Chat(Base):
    __tablename__ = 'chats'

    id: UUID
    title: str
    description: str | None
    user_id: UUID
    created_at: datetime
```

**Relations:**

- `user:` Foreign key to `User` table.
- `kmeans_datas:` One-to-many relationship to `KmeansData`.

## Schemas

The package includes the following Pydantic schemas:

- `ChatCreate:` Schema for creating a new
chat.
- `ChatUpdateFull:` Schema for full update
of a chat.
- `ChatUpdatePartial:` Schema for partial
update of a chat.
- `ChatRead:` Schema for reading chat details.

**Example:**

```python
chat_create = ChatCreate(title="My Chat", description="Example chat")
```

## CRUD Functions

CRUD operations are implemented using SQLAlchemy async sessions:

- `create_chat(db, user_id, chat_scheme):` Create a new chat.
- `read_chat(db, chat_id):` Retrieve a chat by ID.
- `get_chats(db, user_id, skip, limit):` Retrieve a paginated list of chats for a user.
- `update_chat(db, chat_id, chat_scheme, exclude_unset=False):` Update a chat (full or partial).
- `delete_chat(db, chat_id):` Delete a chat.

**Example:**

```python
chat = await crud.create_chat(db, user_id, chat_create)
```

## API Routes

- `POST /chat/` — Create a chat.
- `GET /chat/{chat_id}` — Retrieve a chat by ID.
- `GET /chat/` — Retrieve list of chats (with pagination: skip, limit).
- `PUT /chat/{chat_id}` — Full update a chat.
- `PATCH /chat/{chat_id}` — Partial update a chat.
- `DELETE /chat/{chat_id}` — Delete a chat.

All routes return JSON responses using `ChatRead`
schema where applicable.

## Authentication

Some routes are protected with a
dependency on `verify_access_token`.
This ensures that only authenticated
users can perform actions like updating
or deleting chats.

Example in `router.py`:

```python
@chat_router.put("/{chat_id}", dependencies=[Depends(verify_access_token)])
async def full_update_chat(...):
    ...
```

## Notes

- Database commits and refreshes are handled
safely in `crud.py`.

- Exceptions are managed using FastAPI
`HTTPException` for 404 and 400 errors.

- Relationships allow linking `Chat` with
`User` and `KmeansData`.