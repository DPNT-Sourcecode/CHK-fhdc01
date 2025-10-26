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

    def get_item_quantity(self, skus: str) -> dict[str, int]:
        return [{"sku": sku, "quantity": skus.count(sku)} for sku in set(skus)]
    
    def calculate_item_price(self, prices: list[Price], item) -> int | None:
        sku_price = next((price for price in prices if price["sku"] == item["sku"]), None)
        if not sku_price:
            return None
        if sku_price["special_offer"] and sku_price["special_offer"]["quantity"] == item["quantity"]:
            return sku_price["special_offer"]["price"]
        return sku_price["price"] * item["quantity"]

    # skus = unicode string
    def checkout(self, skus):
        totals = []
        prices = self.get_prices()
        item_with_quantity = self.get_item_quantity(skus)
        for item in item_with_quantity:
            totals.append(self.calculate_item_price(prices, item))
        if None in totals:
            return -1
        return sum(totals)

