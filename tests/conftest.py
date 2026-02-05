from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.orm import Session

from src.app.infrastructure.db import Database, get_db
from src.app.infrastructure.models import UserORM
from src.config import Settings, get_settings
from src.app.main import app


@pytest.fixture(scope="function")
def test_db(test_settings) -> Generator[Session, Any, None]:
    """In-memory SQLite для тестов"""
    db = Database(
        settings=test_settings,
        echo=False,
        pool_class=StaticPool,
    )
    db.create_all()
    session = db.create_session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(test_settings, test_db):

    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_settings] = lambda x: test_settings
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def user_factory(client):
    def _make(email: str, password: str, full_name: str) -> UserORM:
        resp = client.post(
            "/auth/register", json={"email": email, "password": password, "full_name": full_name}
        )
        return resp.json()

    return _make


@pytest.fixture(scope="function")
def test_settings(monkeypatch):
    """Фейковые настройки для тестов"""
    monkeypatch.setenv("SECRET_KEY", "tests-secret")
    monkeypatch.setenv("ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "5")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("CONNECT_ARGS", '{"check_same_thread": false}')

    # можно создавать отдельный экземпляр Settings
    return Settings()


@pytest.fixture(scope="function")
def auth_token(user_factory, client):
    email = "aa@g.com"
    password = "lkjsaoiwhghb%iog535bajb"
    full_name = "I'm the best user!"

    _ = user_factory(email, password, full_name)
    response = client.post("/auth/login", data={"username": email, "password": password})
    return response.json()

@pytest.fixture(scope="function")
def auth_headers(auth_token, client):
    token = auth_token["access_token"]
    return {"Authorization": f"Bearer {token}"}