from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict

import postservice_pb2


class Post(BaseModel):
    id: UUID
    title: str
    description: str
    creator_id: str
    created_at: datetime
    updated_at: datetime
    is_private: bool
    tags: List[str]
    views: int
    likes: int

    model_config = ConfigDict(from_attributes=True, extra="allow")

    def to_proto(self) -> postservice_pb2.Post:
        return postservice_pb2.Post(
            id=str(self.id),
            title=self.title,
            description=self.description,
            creator_id=self.creator_id,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),
            is_private=self.is_private,
            tags=self.tags,
            views=self.views,
            likes=self.likes,
        )


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


class Comment(BaseModel):
    id: UUID
    post_id: UUID
    user_id: str
    text: str
    created_at: datetime

    def to_proto(self) -> postservice_pb2.Comment:
        return postservice_pb2.Comment(
            id=str(self.id),
            post_id=str(self.post_id),
            user_id=self.user_id,
            text=self.text,
            created_at=self.created_at.isoformat()
        )

class CommentCreate(BaseModel):
    post_id: UUID
    user_id: UUID
    text: str
