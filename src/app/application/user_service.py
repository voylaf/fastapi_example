from typing import Tuple, Optional, List

from pydantic import EmailStr

from src.app.domain.user_repository import UserRepository
from src.app.infrastructure.models import UserORM
from src.app.domain.user import User
from src.app.interfaces.schemas import UserCreate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(
        self, email: str, password: str, full_name: Optional[str], role: str = 'user'
    ) -> Tuple[str, UserORM]:
        user = UserCreate(email=email, password=password, full_name=full_name, role=role)
        return self.repo.create_user(user)

    async def authenticate_user(self, email: str, password: str) -> Optional[UserORM]:
        return self.repo.authenticate_user(email, password)

    async def list_items(self) -> List[User]:
        return self.repo.list()
