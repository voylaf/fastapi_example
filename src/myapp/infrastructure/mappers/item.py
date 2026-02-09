from dataclasses import asdict
from src.myapp.domain.item import Item
from src.myapp.infrastructure.models.item import ItemORM


def to_domain(model: ItemORM) -> Item:
    return Item(**{field: getattr(model, field) for field in Item.__dataclass_fields__})


def to_model(item: Item) -> ItemORM:
    data = asdict(item)
    data.pop("id", None)
    return ItemORM(**data)
