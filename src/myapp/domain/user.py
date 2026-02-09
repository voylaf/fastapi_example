from dataclasses import dataclass, replace
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class User:
    id: UUID
    email: str
    hashed_password: str
    role: str
    full_name: Optional[str] = None

    def update_email(self, email: str) -> User:
        return replace(self, email=email)

    def update_hashed_password(self, hashed_password: str) -> User:
        return replace(self, hashed_password=hashed_password)

    def update_role(self, role: str) -> User:
        return replace(self, role=role)

    def update_full_name(self, full_name: str) -> User:
        return replace(self, full_name=full_name)
