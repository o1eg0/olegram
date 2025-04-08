from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

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

class PostList(BaseModel):
    posts: List[Post] = Field(..., description="Список постов")
    total_count: int = Field(..., description="Общее количество постов")
