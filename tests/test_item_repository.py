import decimal

import pytest
from hypothesis import given
import hypothesis.strategies as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.myapp.infrastructure.db import Base
from orm.item_repository_sqlalchemy import ItemRepositorySQLAlchemy
from src.myapp.infrastructure.models.item import ItemORM


# Генерируем случайные Item
@given(
    name=st.text(min_size=1, max_size=20),
    description=st.text(max_size=50),
    price=st.floats(min_value=0, max_value=1000).map(decimal.Decimal),
    tax=st.floats(min_value=0, max_value=100).map(decimal.Decimal),
    uuid=st.uuids(),
)
def test_add_and_list_items(name, description, price, tax, uuid):
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()
    repo = ItemRepositorySQLAlchemy(db_session)
    item = ItemORM(name=name, description=description, price=price, tax=tax)
    uuid, added_item = repo.add(item, owner_id=uuid)
    assert added_item is not None
    items = repo.list()

    # Проверяем invariants
    assert added_item in items
    assert added_item.name == name
    assert added_item.description == description
    assert added_item.price == pytest.approx(round(price, 2), rel=1e-9)
    assert added_item.tax == pytest.approx(round(tax, 2), rel=1e-9)
