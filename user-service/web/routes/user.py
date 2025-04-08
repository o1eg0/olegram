import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from repositories.base import UserRepository
from passlib.context import CryptContext

from repositories.schemas import UserCreate, User, UserVerify
from token_service import TokenService
from web.dependencies import get_user_repository, get_pwd_context, get_token_service, get_username_by_token

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", response_model=User)
async def register(
    user_create: UserCreate,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    pwd_context: Annotated[CryptContext, Depends(get_pwd_context)],
):
    hashed = pwd_context.hash(user_create.password)
    user = await user_repository.get_by_login(user_create.login)
    if user is not None:
        raise HTTPException(
            status_code=400, detail="User with this username already exists"
        )

    user = await user_repository.create(user_create, hashed)
    if not user:
        raise HTTPException(status_code=500, detail="Failed to create user")
    return user


@router.post("/auth")
async def auth(
    user_verify: UserVerify,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    pwd_context: Annotated[CryptContext, Depends(get_pwd_context)],
    token_service: Annotated[TokenService, Depends(get_token_service)]
):
    if not (
        await user_repository.verify(
            user_verify.username, user_verify.password, pwd_context
        )
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "status": "success",
        "access_token": token_service.create_access_token(user_verify.username),
        "token_type": "bearer",
    }


@router.get("/validate")
async def validate(username: Annotated[str, Depends(get_username_by_token)]):
    if username is None:
        return {"status": "invalid"}
    return {"status": "success", "username": username}
