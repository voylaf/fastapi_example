from typing import Generator, Optional, cast

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import ColumnElement, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import Settings
from src.myapp.application import auth
from src.myapp.infrastructure.models.user import UserORM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_settings() -> Settings:
    return Settings()


def get_db(settings: Settings = Depends(get_settings)) -> Generator[Session, None, None]:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=settings.connect_args or {},
    )
    SessionLocal = sessionmaker(bind=engine)

    db = SessionLocal()
    assert isinstance(db, Session)
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> UserORM:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = auth.decode_access_token(token, settings=settings)

    if token_data is None:
        raise credentials_exception
    user_orm: Optional[UserORM] = (
        db.query(UserORM)
        .filter(cast(ColumnElement[bool], UserORM.id == token_data.user_id))
        .first()
    )
    if user_orm is None:
        raise credentials_exception
    return user_orm
