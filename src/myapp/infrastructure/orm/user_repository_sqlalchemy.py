from typing import cast, Optional, List

from sqlalchemy import ColumnElement, select
from sqlalchemy.orm import Session

from src.myapp.infrastructure.models.user import UserORM
from src.myapp.application.auth import get_password_hash
from src.myapp.infrastructure.repositories.user_repository import UserRepository
from src.myapp.interfaces import schemas
from src.myapp.application.auth import verify_password


class UserRepositorySQLAlchemy(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_create: schemas.UserCreate) -> UserORM:
        hashed_password = get_password_hash(user_create.password)
        user = UserORM(email=user_create.email,
                       hashed_password=hashed_password,
                       full_name=user_create.full_name,
                       role=user_create.role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, email: str, password: str) -> Optional[UserORM]:
        user: Optional[UserORM] = (
            self.db.query(UserORM)
            .filter(cast(ColumnElement[bool], UserORM.email == email))
            .first()
        )
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None
        return user

    def list(self) -> List[UserORM]:
        stmt = select(UserORM)
        return list(self.db.scalars(stmt).all())
