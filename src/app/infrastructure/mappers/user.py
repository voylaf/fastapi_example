from dataclasses import asdict

from src.app.infrastructure.models.user import UserORM
from user import User


def to_domain(model: UserORM) -> User:
    return User(**{field: getattr(model, field) for field in User.__dataclass_fields__})


def to_model(user: User) -> UserORM:
    data = asdict(user)
    data.pop("id", None)
    return UserORM(**data)
