from abc import ABC, abstractmethod
from uuid import UUID

from repositories.schemas import PostCreate, Post, PostUpdate, Comment, CommentCreate


class PostRepository(ABC):
    @abstractmethod
    async def create(self, post: PostCreate) -> Post:
        pass

    @abstractmethod
    async def get(self, post_id: UUID) -> Post | None:
        pass

    @abstractmethod
    async def update(self, post_id: UUID, post: PostUpdate) -> Post | None:
        pass

    @abstractmethod
    async def delete(self, post_id: UUID) -> bool:
        pass

    @abstractmethod
    async def list_posts(self, creator_id: str, offset: int, limit: int) -> tuple[list[Post], int]:
        pass

    @abstractmethod
    async def like(self, post_id: UUID) -> bool:
        pass

    @abstractmethod
    async def view(self, post_id: UUID) -> bool:
        pass


class CommentRepository(ABC):
    @abstractmethod
    async def create(self, comment: CommentCreate) -> Comment:
        pass

    @abstractmethod
    async def list_comments(self, post_id: UUID, offset: int, limit: int) -> tuple[list[Comment], int]:
        pass
