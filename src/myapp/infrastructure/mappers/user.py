from dataclasses import asdict

from user import User

from src.myapp.infrastructure.models.user import UserORM


def to_domain(model: UserORM) -> User:
    return User(**{field: getattr(model, field) for field in User.__dataclass_fields__})


def to_model(user: User) -> UserORM:
    data = asdict(user)
    data.pop("id", None)
    return UserORM(**data)
