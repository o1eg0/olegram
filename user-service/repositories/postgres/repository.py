import uuid
from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from repositories.postgres.models import User as DBUser, Base
from repositories.base import UserRepository
from repositories.schemas import UserCreate, User, UserProfileUpdate, UserProfile


class PostgresUserRepository(UserRepository):
    def __init__(self, dns: str):
        self.engine = create_async_engine(dns, echo=False, future=True)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get(self, user_id: UUID) -> User | None:
        async with self.async_session() as session:
            result = await session.execute(select(DBUser).where(DBUser.id == user_id))
            db_user = result.scalar_one_or_none()
        return User.model_validate(db_user)

    async def verify(
        self, login: str, password: str, pwd_context: CryptContext
    ) -> bool:
        async with self.async_session() as session:
            result = await session.execute(select(DBUser).where(DBUser.login == login))
            db_user = result.scalar_one_or_none()

        if not db_user:
            return False
        return pwd_context.verify(secret=password, hash=db_user.password_hash)

    async def create(self, user: UserCreate, hashed_password: str) -> User | None:
        user_dict = user.model_dump(exclude={"password"})

        db_user = DBUser(**user_dict, password_hash=hashed_password, id=uuid.uuid4())
        async with self.async_session() as session, session.begin():
            session.add(db_user)
        return User.model_validate(db_user)

    async def get_by_login(self, login: str) -> User | None:
        async with self.async_session() as session:
            result = await session.execute(select(DBUser).where(DBUser.login == login))
            db_user = result.scalar_one_or_none()

        return User.model_validate(db_user) if db_user else None

    async def update_profile(
        self, login: str, profile: UserProfileUpdate
    ) -> UserProfile | None:
        async with self.async_session() as session:
            result = await session.execute(select(DBUser).where(DBUser.login == login))
            db_user = result.scalar_one_or_none()

            if not db_user:
                return None

            update_data = profile.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                if value is not None:
                    setattr(db_user, field, value)

            await session.commit()
            await session.refresh(db_user)

        return UserProfile.model_validate(db_user)
