import os
from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.myapp.application.deps import get_db, get_settings
from src.myapp.infrastructure.models.user import UserORM
from src.myapp.infrastructure.db import Base
from src.config import Settings
from src.myapp.main import app


@pytest.fixture(scope="session")
def test_settings():
    """Фейковые настройки для тестов"""
    os.environ["SECRET_KEY"] = "tests-secret"
    os.environ["ALGORITHM"] = "HS256"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "5"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["CONNECT_ARGS"] = '{"check_same_thread": false}'

    # можно создавать отдельный экземпляр Settings
    return Settings()


@pytest.fixture(scope="session")
def engine(test_settings):
    engine = create_engine(
        test_settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_db(engine) -> Generator[Session, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(test_settings, test_db):

    def override_get_db() -> Generator[Session, Any, None]:
        yield test_db

    app.dependency_overrides[get_settings] = lambda: test_settings
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
