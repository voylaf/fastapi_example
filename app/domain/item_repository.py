from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from uuid import UUID

from .item import Item
from ..infrastructure.models import ItemORM


class ItemRepository(ABC):
    @abstractmethod
    def add(self, item: Item, owner_id: UUID) -> Tuple[UUID, ItemORM]: ...

    @abstractmethod
    def get(self, item_id: UUID) -> Optional[ItemORM]: ...

    @abstractmethod
    def list(self) -> List[ItemORM]: ...
