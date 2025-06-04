import pytest, asyncio
from fastapi.testclient import TestClient
from user_service.main import create_app
from repositories.postgres.repository import PostgresUserRepository


@pytest.fixture
def test_client(pg_container, monkeypatch):
    app = create_app()

    repo = PostgresUserRepository(pg_container.get_connection_url())
    asyncio.get_event_loop().run_until_complete(repo.create_tables())

    app.dependency_overrides[PostgresUserRepository] = lambda: repo
    return TestClient(app)
