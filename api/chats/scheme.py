from pydantic import BaseModel, Field
from uuid import UUID


class ChatCreate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    title: str = Field(min_length=1, max_length=256)
    description: str | None = None


class ChatUpdateFull(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    title: str = Field(min_length=1, max_length=256)
    description: str = Field(min_length=1)


class ChatUpdatePartial(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    title: str | None = Field(None, max_length=256)
    description: str | None = None


class ChatRead(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    title: str
    description: str | None = None