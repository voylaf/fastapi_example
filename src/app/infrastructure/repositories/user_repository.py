from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from src.app.infrastructure.models import user
from src.app.interfaces.schemas import UserCreate


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate) -> Tuple[str, UserORM]: ...

    @abstractmethod
    def authenticate_user(self, email: str, password: str) -> Optional[UserORM]: ...

    @abstractmethod
    def list(self) -> List[UserORM]: ...