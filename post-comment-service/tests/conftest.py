import psycopg2
import pytest

from repositories.postgres.repository import PostgresPostRepository

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
async def post_repository(setup_test_db):
    repository = PostgresPostRepository(TEST_DB_DNS)
    await repository.create_tables()
    return repository
