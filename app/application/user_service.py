from typing import Tuple, Optional, List

from pydantic import EmailStr

from app.domain.user_repository import UserRepository
from app.infrastructure.models import UserORM
from ..domain.user import User
from ..interfaces.schemas import UserCreate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, email: str, password: str, full_name: Optional[str], role: str = 'user') -> Tuple[str, UserORM]:
        user = UserCreate(email=email, password=password, full_name=full_name, role=role)
        return self.repo.create_user(user)

    def authenticate_user(self, email: str, password: str) -> Optional[UserORM]:
        return self.repo.authenticate_user(email, password)

    def list_items(self) -> List[User]:
        return self.repo.list()
