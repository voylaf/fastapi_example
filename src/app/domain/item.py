from dataclasses import dataclass, replace
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class Item:
    name: str
    price: Decimal
    tax: Optional[Decimal] = None
    description: Optional[str] = None

    def __post_init__(self):
        object.__setattr__(self, "tax", self.tax or Decimal("0.00"))
        object.__setattr__(
            self,
            "description",
            self.description or f"{self.name} with price {self.price} (Tax = {self.tax}%)",
        )

    def calc_price_with_tax(self) -> Decimal:
        return self.price * (1 + self.tax / 100)

    def update_price(self, price: Decimal) -> Item:
        return replace(self, price=price)

    def update_name(self, name: str) -> Item:
        return replace(self, name=name)

    def update_tax(self, tax: Decimal) -> Item:
        return replace(self, tax=tax)

    def update_description(self, description: str) -> Item:
        return replace(self, description=description)

    def apply_discounts(self, discount: Decimal) -> Item:
        return replace(self, price=self.price * discount)
