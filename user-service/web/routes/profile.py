import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from repositories.base import UserRepository
from repositories.schemas import UserProfile, UserProfileUpdate
from web.dependencies import get_user_repository

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/{username}/profile", response_model=UserProfile)
async def get_profile(
    username: str,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    profile = await user_repository.get_profile_by_login(username)
    if not profile:
        raise HTTPException(404, "User not found")
    return profile


@router.put("/{username}/profile", response_model=UserProfile)
async def update_profile(
    username: str,
    profile_update: UserProfileUpdate,
    user_repository: UserRepository = Depends(get_user_repository),
):
    profile = await user_repository.update_profile(username, profile_update)
    if not profile:
        raise HTTPException(404, "User not found")
    return profile
