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
        prices = self.get_prices()
        sku_with_quantity = self.get_sku_quantity(skus)
        for sku in sku_with_quantity:
            if sku["sku"] not in prices:
                return -1
            if prices:
        raise NotImplementedError()



