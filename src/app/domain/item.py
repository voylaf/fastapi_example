class Item:
    def __init__(self, name: str, price: float, tax: float | None = None):
        self.name = name
        self.price = price
        self.tax = tax or 0.0

    def calc_price_with_tax(self) -> float:
        return self.price * (1 + self.tax / 100)