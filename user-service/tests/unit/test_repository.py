import pytest
from passlib.context import CryptContext

from repositories.schemas import UserCreate, UserProfileUpdate


@pytest.mark.asyncio
async def test_create_and_get_user(user_repository):
    user_data = UserCreate(
        login="test_user", password="secret", email="test_user@example.com"
    )
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user_data.password)

    created_user = await user_repository.create(user_data, hashed_password)
    assert created_user is not None
    assert created_user.login == "test_user"
    assert created_user.email == "test_user@example.com"
    assert created_user.id is not None

    user_from_db = await user_repository.get(created_user.id)
    assert user_from_db is not None
    assert user_from_db.login == created_user.login


@pytest.mark.asyncio
async def test_get_by_login(user_repository):
    user_data = UserCreate(
        login="test_user_2", password="secret2", email="test_user2@example.com"
    )
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user_data.password)
    _ = await user_repository.create(user_data, hashed_password)

    user = await user_repository.get_by_login("test_user_2")
    assert user is not None
    assert user.login == "test_user_2"
    assert user.email == "test_user2@example.com"


@pytest.mark.asyncio
async def test_verify(user_repository):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    user_data = UserCreate(
        login="test_user_verify",
        password="secret_verify",
        email="test_verify@example.com",
    )
    hashed_password = pwd_context.hash(user_data.password)
    await user_repository.create(user_data, hashed_password)

    is_valid = await user_repository.verify(
        "test_user_verify", "secret_verify", pwd_context
    )
    assert is_valid is True

    is_valid_wrong_password = await user_repository.verify(
        "test_user_verify", "wrong", pwd_context
    )
    assert is_valid_wrong_password is False

    is_valid_unknown_user = await user_repository.verify(
        "unknown", "secret", pwd_context
    )
    assert is_valid_unknown_user is False


@pytest.mark.asyncio
async def test_update_profile(user_repository):
    from repositories.schemas import UserCreate

    user_data = UserCreate(
        login="user_for_update", password="1234", email="upd_user@example.com"
    )
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user_data.password)
    await user_repository.create(user_data, hashed_password)

    profile_update = UserProfileUpdate(
        first_name="Pudge",
        last_name="Shadow fiend",
        phone_number="88005553535",
        bio="NewBio",
    )

    updated_profile = await user_repository.update_profile(
        "user_for_update", profile_update
    )
    assert updated_profile is not None
    assert updated_profile.first_name == "Pudge"
    assert updated_profile.last_name == "Shadow fiend"
    assert updated_profile.phone_number == "88005553535"
    assert updated_profile.bio == "NewBio"

    updated_profile_none = await user_repository.update_profile(
        "no_user", profile_update
    )
    assert updated_profile_none is None
