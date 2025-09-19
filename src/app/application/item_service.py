from typing import List, Tuple, Optional
from uuid import UUID

from src.app.domain.item import Item
from src.app.domain.item_repository import ItemRepository
from src.app.infrastructure.models import ItemORM


class ItemService:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    def create_item(
        self, name: str, price: float, tax: Optional[float], owner_id: Optional[UUID]
    ) -> Tuple[UUID, ItemORM]:
        item = Item(name=name, price=price, tax=tax)
        return self.repo.add(item, owner_id)

    def get_item(self, item_id: UUID) -> Optional[ItemORM]:
        return self.repo.get(item_id)

    def list_items(self) -> List[ItemORM]:
        return self.repo.list()
