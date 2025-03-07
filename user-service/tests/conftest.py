import os
import pytest
import psycopg2
from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import create_app
from repositories.postgres.repository import PostgresUserRepository

TEST_DB_NAME = "test_db"
TEST_DB_USER = "postgres"
TEST_DB_PASS = "postgres"
TEST_DB_HOST = "localhost"
TEST_DB_PORT = "5432"

MAIN_DB_DNS = (
    f"postgresql://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/postgres"
)
TEST_DB_DNS = f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"


@pytest.fixture(scope="function")
def setup_test_db():
    conn = psycopg2.connect(
        dbname="postgres",
        user=TEST_DB_USER,
        password=TEST_DB_PASS,
        host=TEST_DB_HOST,
        port=TEST_DB_PORT,
    )
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME} WITH (FORCE);")
    cur.execute(f"CREATE DATABASE {TEST_DB_NAME};")

    cur.close()
    conn.close()

    yield

    conn = psycopg2.connect(
        dbname="postgres",
        user=TEST_DB_USER,
        password=TEST_DB_PASS,
        host=TEST_DB_HOST,
        port=TEST_DB_PORT,
    )
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME} WITH (FORCE);")
    cur.close()
    conn.close()


@pytest.fixture(scope="function")
def app(setup_test_db) -> FastAPI:
    os.environ["DB_DNS"] = TEST_DB_DNS

    application = create_app()
    return application


@pytest.fixture(scope="function")
def client(app: FastAPI):
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
async def user_repository(setup_test_db):
    repository = PostgresUserRepository(TEST_DB_DNS)
    await repository.create_tables()
    return repository
