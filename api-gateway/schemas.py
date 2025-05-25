from datetime import datetime, date
from typing import List

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(..., description="Заголовок поста")
    description: str = Field(..., description="Описание поста")
    is_private: bool = Field(default=False, description="Приватность поста")
    tags: List[str] = Field(default_factory=list, description="Теги поста")


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: str = Field(..., description="Уникальный идентификатор поста")
    creator_id: str = Field(..., description="ID пользователя-создателя поста")
    created_at: datetime = Field(..., description="Дата и время создания поста")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления поста")
    likes: int = Field(..., description="Лайки поста")
    views: int = Field(..., description="Просмотры")


class PostList(BaseModel):
    posts: List[Post] = Field(..., description="Список постов")
    total_count: int = Field(..., description="Общее количество постов")


class Comment(BaseModel):
    id: str
    post_id: str
    user_id: str
    text: str
    created_at: datetime


class CommentList(BaseModel):
    comments: List[Comment] = Field(..., description="Список комментариев")
    total_count: int = Field(..., description="Общее количество комментариев")


class Counter(BaseModel):
    views: int
    likes: int
    comments: int

class TimelinePoint(BaseModel):
    date: date
    value: int

class TimelineResponse(BaseModel):
    points: list[TimelinePoint]

class TopItem(BaseModel):
    id: str
    value: int
