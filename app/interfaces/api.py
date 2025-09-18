from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from ..application.auth import create_access_token
from ..application.deps import get_current_user
from ..application.item_service import ItemService
from ..application.user_service import UserService
from ..infrastructure.db import get_db
from ..infrastructure.item_repository_sqlalchemy import ItemRepositorySQLAlchemy
from .schemas import ItemCreate, ItemResponse, UserResponse, UserCreate
from ..infrastructure.models import UserORM
from ..infrastructure.user_repository_sqlalchemy import UserRepositorySQLAlchemy

router = APIRouter()


@router.post("/items", response_model=ItemResponse)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    repo = ItemRepositorySQLAlchemy(db)
    service = ItemService(repo)
    owner_id = current_user.id
    item_id, new_item = service.create_item(item.name, item.price, item.tax, owner_id)
    return ItemResponse(id=item_id, owner_id=owner_id, **item.model_dump())


@router.get("/items", response_model=List[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    repo = ItemRepositorySQLAlchemy(db)
    service = ItemService(repo)
    return service.list_items()


@router.post("/auth/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepositorySQLAlchemy(db)
    service = UserService(repo)
    return service.create_user(user.email, user.password, user.full_name, user.role)


@router.post("/auth/login", response_model=Dict)
def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    repo = UserRepositorySQLAlchemy(db)
    service = UserService(repo)
    user: UserORM = service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
