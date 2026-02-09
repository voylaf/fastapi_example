from typing import List, Optional, Tuple

from src.myapp.domain.user import User
from src.myapp.infrastructure.models.user import UserORM
from src.myapp.infrastructure.repositories.user_repository import UserRepository
from src.myapp.interfaces.schemas import UserCreate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(
        self, email: str, password: str, full_name: Optional[str], role: str = "user"
    ) -> Tuple[str, UserORM]:
        user = UserCreate(email=email, password=password, full_name=full_name, role=role)
        return self.repo.create_user(user)

    def authenticate_user(self, email: str, password: str) -> Optional[UserORM]:
        return self.repo.authenticate_user(email, password)

    def list_items(self) -> List[User]:
        return self.repo.list()
