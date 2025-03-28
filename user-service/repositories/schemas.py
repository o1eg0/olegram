from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class User(BaseModel):
    id: UUID
    login: str
    email: str
    first_name: str | None
    last_name: str | None
    birthday: date | None
    bio: str | None
    avatar_url: str | None
    phone_number: str | None

    model_config = ConfigDict(from_attributes=True, extra="allow")


class UserProfile(BaseModel):
    email: str = Field(description="Электронная почта")
    first_name: str | None = Field(description="Имя пользователя")
    last_name: str | None = Field(description="Фамилия пользователя")
    birthday: date | None = Field(description="Дата рождения")
    bio: str | None = Field(description='Текст "О себе"')
    avatar_url: str | None = Field(description="Ссылка на аватар")
    phone_number: str | None = Field(description="Номер телефона")

    model_config = ConfigDict(
        from_attributes=True,
        extra="allow",
    )


class UserCreate(BaseModel):
    login: str = Field(description="Логин пользователя в системе")
    password: str = Field(description="Пароль, храниться в защифрованном виде")
    email: str = Field(description="Электронная почта")


class UserProfileUpdate(BaseModel):
    email: str | None = Field(default=None, description="Электронная почта")
    first_name: str | None = Field(default=None, description="Имя пользователя")
    last_name: str | None = Field(default=None, description="Фамилия пользователя")
    birthday: date | None = Field(default=None, description="Дата рождения")
    bio: str | None = Field(default=None, description='Текст "О себе"')
    avatar_url: str | None = Field(default=None, description="Ссылка на аватар")
    phone_number: str | None = Field(default=None, description="Номер телефона")


class UserVerify(BaseModel):
    username: str = Field(description="Логин пользователя в системе")
    password: str = Field(description="Пароль пользователя для подтверждения")
