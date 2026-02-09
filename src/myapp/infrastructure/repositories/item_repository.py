from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from uuid import UUID

from src.myapp.infrastructure.models.item import ItemORM


class ItemRepository(ABC):
    @abstractmethod
    def add(self, item: ItemORM, owner_id: UUID) -> Tuple[UUID, ItemORM]: ...

    @abstractmethod
    def get(self, item_id: UUID) -> Optional[ItemORM]: ...

    @abstractmethod
    def list(self) -> List[ItemORM]: ...
