from uuid import UUID

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Annotated

from regex import regex


# API-контракты


class ItemCreate(BaseModel):
    name: Annotated[str, Field(max_length=127), "Maximal length of name is 127 symbols."]
    price: float
    tax: Optional[float]
    description: Annotated[
        Optional[str], Field(max_length=1023), "Maximal length of description is 1023 symbols."
    ] = None
    price: Annotated[float, Field(gt=-1e9, lt=1e10), "Price is between -10e9 and 10e15."]
    tax: Annotated[
        Optional[float], Field(gt=-100, lt=1e5), "Tax is between -100 and 10e6 percentage."
    ] = None


class ItemResponse(ItemCreate):
    id: UUID
    owner_id: UUID

    model_config = {"from_attributes": True}


class TokenData(BaseModel):
    user_id: UUID


class UserCreate(BaseModel):
    model_config = {"from_attributes": True}
    email: EmailStr
    full_name: Optional[str] = (
        Annotated[
            str,
            Field(pattern=r"^[\p{L}0-9~!?@#$%^&*_\-+()\[\]{}></'|.,:; ]*$"),
        ]
        | None
    )
    password: Annotated[
        str,
        Field(
            min_length=12,
            max_length=128,
            pattern=regex.compile(
                r"""^[\p{L}0-9~!?@#$%^&*_\-+()\[\]{}></|\"'.,:;]{12,128}$"""
            ).pattern,
        ),
        """Minimal length of password is between 12 and 128 symbols. It may contain letters, numbers and special characters: ~!?@#$%^&*_-+"'()[]{}></|.,:;""",
    ]
    role: str = "user"


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str] = None
    role: str

    model_config = {"from_attributes": True}
