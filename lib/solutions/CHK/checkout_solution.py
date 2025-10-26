import json

from typing import TypedDict

class Price(TypedDict):
    sku: str
    quantity: int
    special_offer: dict | None

class CheckoutSolution:

    def get_prices(self) -> list[Price]:
        with open("lib/solutions/CHK/prices.json") as f:
            prices: list[Price] = json.load(f)
        return prices

    def get_sku_quantity(self, skus: str) -> dict[str, int]:
        return [{"sku": sku, "quantity": skus.count(sku)} for sku in set(skus)]

    # skus = unicode string
    def checkout(self, skus):
        totals = []
        prices = self.get_prices()
        sku_with_quantity = self.get_sku_quantity(skus)
        for sku in sku_with_quantity:
            sku_price = next((price for price in prices if price["sku"] == sku["sku"]), None)
            if not sku_price:
                return -1
            totals += sku_price["special_offer"]["price"] if \
                sku_price["special_offer"]["quantity"] == sku["quantity"] else sku_price["price"]
        return sum(totals)





