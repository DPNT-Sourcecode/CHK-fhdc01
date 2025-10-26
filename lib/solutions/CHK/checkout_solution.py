import json

from typing import TypedDict

class Sku(TypedDict):
    sku: str
    quantity: int
    special_offer: dict | None

class CheckoutSolution:

    # skus = unicode string
    def checkout(self, skus):
        prices = None
        with open("lib/solutions/CHK/prices.json") as f:
            prices = json.load(f)
        sku_with_quantity = [{"sku": sku, "quantity": skus.count(sku)} for sku in set(skus)]
        for sku in sku_with_quantity:
            if sku["sku"] not in prices:
                return -1
            if prices[sku][]
        raise NotImplementedError()


