from typing import Tuple, Optional, cast
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import ColumnElement, select
from sqlalchemy.orm import Session
from src.app.domain.item import Item
from src.app.domain.item_repository import ItemRepository
from src.app.infrastructure.models import ItemORM


class ItemRepositorySQLAlchemy(ItemRepository):
    def __init__(self, db: Session):
        if db is None:
            raise HTTPException(status_code=404, detail="database not found")
        self.db = db

    def add(self, item: Item, owner_id: UUID) -> Tuple[UUID, ItemORM]:
        orm = ItemORM(name=item.name, price=item.price, tax=item.tax, owner_id=owner_id)
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return orm.id, orm

    def get(self, item_id: UUID) -> Optional[ItemORM]:
        orm = (
            self.db.query(ItemORM).filter(cast(ColumnElement[bool], ItemORM.id == item_id)).first()
        )
        return orm

    def list(self) -> list[ItemORM]:
        stmt = select(ItemORM)
        return list(self.db.scalars(stmt).all())
