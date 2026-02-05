from typing import List, Dict, Tuple
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from config import Settings, get_settings
from src.app.application.auth import create_access_token
from src.app.application.deps import get_current_user
from src.app.application.item_service import ItemService
from src.app.application.user_service import UserService
from src.app.infrastructure.db import get_db
from src.app.infrastructure.item_repository_sqlalchemy import ItemRepositorySQLAlchemy
from src.app.interfaces.schemas import ItemCreate, ItemResponse, UserResponse, UserCreate
from src.app.infrastructure.models import UserORM, ItemORM
from src.app.infrastructure.user_repository_sqlalchemy import UserRepositorySQLAlchemy

router = APIRouter()


@router.post("/items", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
) -> ItemResponse:
    repo = ItemRepositorySQLAlchemy(db)
    service = ItemService(repo)
    owner_id = current_user.id
    item_with_id: Tuple[UUID, ItemORM] = await service.create_item(
        item.name, item.price, item.tax, owner_id
    )
    item_id, new_item = item_with_id
    return ItemResponse(id=item_id, owner_id=owner_id, **item.model_dump())


@router.get("/items", response_model=List[ItemResponse])
async def get_items(db: Session = Depends(get_db)) -> List[ItemORM]:
    repo = ItemRepositorySQLAlchemy(db)
    service = ItemService(repo)
    items = await service.list_items()
    return items


@router.post("/auth/register", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> Tuple[str, UserORM]:
    repo = UserRepositorySQLAlchemy(db)
    service = UserService(repo)
    result = await service.create_user(user.email, user.password, user.full_name, user.role)
    return result


@router.post("/auth/login", response_model=Dict)
async def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    repo = UserRepositorySQLAlchemy(db)
    service = UserService(repo)
    user: UserORM = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)}, settings=settings)
    return {"access_token": access_token, "token_type": "bearer"}
