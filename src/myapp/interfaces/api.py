from decimal import Decimal
from typing import List, Dict, Tuple
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from src.config import Settings
from src.myapp.application.auth import create_access_token
from src.myapp.application.deps import get_current_user, get_db, get_settings
from src.myapp.services.item_service import ItemService
from src.myapp.services.user_service import UserService
from src.myapp.infrastructure.orm.item_repository_sqlalchemy import ItemRepositorySQLAlchemy
from src.myapp.interfaces.schemas import ItemCreate, ItemResponse, UserResponse, UserCreate
from src.myapp.infrastructure.models.item import ItemORM
from src.myapp.infrastructure.models.user import UserORM
from src.myapp.infrastructure.orm.user_repository_sqlalchemy import UserRepositorySQLAlchemy

router = APIRouter()


@router.post("/items", response_model=ItemResponse)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
) -> ItemResponse:
    repo = ItemRepositorySQLAlchemy(db)
    service = ItemService(repo)
    owner_id = current_user.id
    item_with_id: Tuple[UUID, ItemORM] = service.create_item(
        item.name, Decimal(item.price), item.tax, owner_id
    )
    item_id, new_item = item_with_id
    return ItemResponse(id=item_id, owner_id=owner_id, **item.model_dump())


@router.get("/items", response_model=List[ItemResponse])
def get_items(db: Session = Depends(get_db)) -> List[ItemORM]:
    repo = ItemRepositorySQLAlchemy(db)
    service = ItemService(repo)
    items = service.list_items()
    return items


@router.post("/auth/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> Tuple[str, UserORM]:
    repo = UserRepositorySQLAlchemy(db)
    service = UserService(repo)
    result = service.create_user(user.email, user.password, user.full_name, user.role)
    return result


@router.post("/auth/login", response_model=Dict)
def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    repo = UserRepositorySQLAlchemy(db)
    service = UserService(repo)
    user: UserORM = service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)}, settings=settings)
    return {"access_token": access_token, "token_type": "bearer"}
