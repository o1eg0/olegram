from uuid import UUID

from sqlalchemy import delete, select, func, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from repositories.base import PostRepository, CommentRepository
from repositories.postgres.models import Post as DBPost, Comment as DBComment, Base
from repositories.schemas import PostCreate, Post, PostUpdate, Comment, CommentCreate


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

    async def like(self, post_id: UUID) -> bool:
        async with self.async_session() as session, session.begin():
            result = await session.execute(
                update(DBPost)
                .where(DBPost.id == post_id)
                .values(likes=DBPost.likes + 1)
                .execution_options(synchronize_session="fetch")
            )
            return result.rowcount > 0

    async def view(self, post_id: UUID) -> bool:
        async with self.async_session() as session, session.begin():
            result = await session.execute(
                update(DBPost)
                .where(DBPost.id == post_id)
                .values(views=DBPost.views + 1)
                .execution_options(synchronize_session="fetch")
            )
            return result.rowcount > 0


class PostgresCommentRepository(CommentRepository):
    def __init__(self, dns: str):
        self.engine = create_async_engine(dns, echo=False, future=True)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_tables(self):
        pass

    async def create(self, comment: CommentCreate) -> Comment:
        async with self.async_session() as session, session.begin():
            db_comment = DBComment(post_id=comment.post_id, user_id=str(comment.user_id), text=comment.text)
            session.add(db_comment)
            await session.flush()
            return Comment.model_validate(db_comment)

    async def list_comments(self, post_id: UUID, offset: int, limit: int) -> tuple[list[Comment], int]:
        async with self.async_session() as session:
            total = await session.scalar(
                select(func.count()).where(DBComment.post_id == post_id)
            )
            result = await session.execute(
                select(DBComment)
                .where(DBComment.post_id == post_id)
                .order_by(DBComment.created_at.asc())
                .offset(offset)
                .limit(limit)
            )
            comments = result.scalars().all()
            return [Comment.model_validate(c) for c in comments], total
