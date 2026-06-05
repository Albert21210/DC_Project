"""Общие pytest-фикстуры."""
import pytest
from fastapi.testclient import TestClient
from packages.core.database import get_connection, init_schema, seed_demo_data
from app.main import app
from app import dependencies


@pytest.fixture
def conn():
    """In-memory БД с демо-данными."""
    c = get_connection(":memory:")
    init_schema(c)
    seed_demo_data(c)
    yield c
    c.close()


@pytest.fixture
def client(conn):
    """TestClient с подменённой БД."""
    app.dependency_overrides[dependencies.get_db] = lambda: conn
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
