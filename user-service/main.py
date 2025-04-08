import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from passlib.context import CryptContext
from token_service import JWTTokenService

from repositories.postgres.repository import PostgresUserRepository
from web.routes.user import router as user_router
from web.routes.profile import router as profile_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    app.state.pwd_context = pwd_context

    jwt_token_service = JWTTokenService(os.getenv("JWT_SECRET"), int(os.getenv("JWT_EXPIRE_TIME")), os.getenv("JWT_ALGO"))
    app.state.token_service = jwt_token_service

    dns = (
        os.getenv("DB_DNS")
        or "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )
    user_repository = PostgresUserRepository(dns)
    await user_repository.create_tables()
    app.state.user_repository = user_repository

    yield


def create_app():
    app = FastAPI(
        title="User Service",
        contact={"name": "Oleg"},
        lifespan=lifespan,
        version="0.1.0",
    )
    app.include_router(user_router, tags=["Users"])
    app.include_router(profile_router, tags=["Profiles"])
    return app
