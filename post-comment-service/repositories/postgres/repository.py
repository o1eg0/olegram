from uuid import UUID

from sqlalchemy import delete, select, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from repositories.base import PostRepository
from repositories.postgres.models import Post as DBPost, Base
from repositories.schemas import PostCreate, Post, PostUpdate


class PostgresPostRepository(PostRepository):
    def __init__(self, dns: str):
        self.engine = create_async_engine(dns, echo=False, future=True)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create(self, post: PostCreate) -> Post:
        async with self.async_session() as session, session.begin():
            db_post = DBPost(**post.model_dump())
            session.add(db_post)
            await session.flush()
            return Post.model_validate(db_post)

    async def get(self, post_id: UUID) -> Post | None:
        async with self.async_session() as session:
            db_post = await session.get(DBPost, post_id)
            return Post.model_validate(db_post) if db_post else None

    async def update(self, post_id: UUID, post: PostUpdate) -> Post | None:
        async with self.async_session() as session, session.begin():
            db_post = await session.get(DBPost, post_id)
            if not db_post:
                return None
            for field, value in post.model_dump(exclude_unset=True).items():
                setattr(db_post, field, value)
            await session.flush()
            return Post.model_validate(db_post)

    async def delete(self, post_id: UUID) -> bool:
        async with self.async_session() as session, session.begin():
            result = await session.execute(delete(DBPost).where(DBPost.id == post_id))
            return result.rowcount > 0

    async def list_posts(self, creator_id: str, offset: int, limit: int) -> tuple[list[Post], int]:
        async with self.async_session() as session:
            total = await session.scalar(select(func.count()).where(DBPost.creator_id == creator_id))
            result = await session.execute(
                select(DBPost).where(DBPost.creator_id == creator_id)
                .offset(offset).limit(limit).order_by(DBPost.created_at.desc())
            )
            posts = result.scalars().all()
            return [Post.model_validate(post) for post in posts], total
