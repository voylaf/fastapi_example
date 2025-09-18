from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.orm import Session

from app.infrastructure.db import Database, get_db
from app.infrastructure.models import UserORM
from main import app


@pytest.fixture(scope="function")
def test_db() -> Generator[Session, Any, None]:
    """In-memory SQLite для тестов"""
    db = Database(
        "sqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},
        pool_class=StaticPool,
    )
    db.create_all()
    session = db.create_session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(test_db):

    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def user_factory(client):
    def _make(email: str, password: str, full_name: str) -> UserORM:
        resp = client.post("/auth/register", json={"email": email, "password": password, "full_name": full_name})
        return resp.json()
    return _make
