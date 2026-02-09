from typing import cast, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session

from src.config import Settings
from src.myapp.infrastructure.models.user import UserORM
from src.myapp.application import auth
from src.myapp.infrastructure.db import Database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_settings() -> Settings:
    return Settings()


def get_db(settings: Settings = Depends(get_settings)):
    db = Database(settings=settings)
    return db.get_db()


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
    else:
        return user_orm
