from decimal import Decimal
from typing import List, Tuple, Optional
from uuid import UUID

from src.app.domain.item import Item
from src.app.infrastructure.repositories.item_repository import ItemRepository
from src.app.infrastructure.models.item import ItemORM
from src.app.infrastructure.mappers.item import to_model


class ItemService:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def create_item(
        self, name: str, price: Decimal, tax: Optional[Decimal], owner_id: Optional[UUID]
    ) -> Tuple[UUID, ItemORM]:
        item = Item(name, price, tax)
        itemORM = to_model(item)
        return self.repo.add(itemORM, owner_id)

    async def get_item(self, item_id: UUID) -> Optional[ItemORM]:
        return self.repo.get(item_id)

    async def list_items(self) -> List[ItemORM]:
        return self.repo.list()
