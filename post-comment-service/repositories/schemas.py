from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Post(BaseModel):
    id: UUID
    title: str
    description: str
    creator_id: str
    created_at: datetime
    updated_at: datetime
    is_private: bool
    tags: List[str]

    model_config = ConfigDict(from_attributes=True, extra="allow")


class PostCreate(BaseModel):
    title: str
    description: str
    creator_id: str
    is_private: bool = False
    tags: List[str] = []


class PostUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_private: bool | None = None
    tags: List[str] | None = None
