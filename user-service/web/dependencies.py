from fastapi import Request
from passlib.context import CryptContext

from repositories.base import UserRepository


def get_user_repository(request: Request) -> UserRepository:
    result = request.app.state.user_repository
    assert isinstance(result, UserRepository)
    return result


def get_pwd_context(request: Request) -> CryptContext:
    result = request.app.state.pwd_context
    assert isinstance(result, CryptContext)
    return result
