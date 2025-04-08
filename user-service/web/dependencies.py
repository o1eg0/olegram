from typing import Annotated

from fastapi import Request, Depends
from fastapi.params import Header
from passlib.context import CryptContext

from repositories.base import UserRepository
from token_service import TokenService


def get_user_repository(request: Request) -> UserRepository:
    result = request.app.state.user_repository
    assert isinstance(result, UserRepository)
    return result


def get_pwd_context(request: Request) -> CryptContext:
    result = request.app.state.pwd_context
    assert isinstance(result, CryptContext)
    return result


def get_token_service(request: Request) -> TokenService:
    result = request.app.state.token_service
    assert isinstance(result, TokenService)
    return result


async def get_username_by_token(
    token_service: Annotated[TokenService, Depends(get_token_service)],
    jwt_token: Annotated[str, Header()],
):
    return token_service.validate_token(jwt_token.replace("Bearer ", ""))
