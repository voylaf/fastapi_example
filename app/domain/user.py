from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str] = None
    hashed_password: str
    role: str