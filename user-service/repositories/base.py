from abc import ABC, abstractmethod
from uuid import UUID

from passlib.context import CryptContext

from repositories.schemas import UserCreate, UserProfileUpdate, User, UserProfile


class UserRepository(ABC):
    @abstractmethod
    async def get(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    async def create(self, user: UserCreate, hashed_password: str) -> User | None:
        pass

    @abstractmethod
    async def verify(
        self, login: str, password: str, pwd_context: CryptContext
    ) -> bool:
        pass

    @abstractmethod
    async def get_by_login(self, login: str) -> User | None:
        pass

    async def get_profile_by_login(self, login: str) -> UserProfile | None:
        user = await self.get_by_login(login)
        return UserProfile(**user.model_dump()) if user else None

    @abstractmethod
    async def update_profile(
        self, login: str, profile: UserProfileUpdate
    ) -> UserProfile | None:
        pass
