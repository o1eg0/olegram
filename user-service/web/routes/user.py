import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from repositories.base import UserRepository
from passlib.context import CryptContext

from repositories.schemas import UserCreate, User, UserVerify
from web.dependencies import get_user_repository, get_pwd_context

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
):
    if not (
        await user_repository.verify(
            user_verify.username, user_verify.password, pwd_context
        )
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"status": "success"}
