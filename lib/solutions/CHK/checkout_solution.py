import json

from .types import Price, BulkOffer, FreeItemOffer

class CheckoutSolution:
    def __init__(self):
        self.skus = []
        self.prices = self.get_prices()
        self.total = 0

    def get_prices(self) -> list[Price]:
        with open("lib/solutions/CHK/prices.json") as f:
            prices: list[Price] = json.load(f)
        return prices

    def get_item_quantity(self, skus: str) -> dict[str, int]:
        return [{"sku": sku, "quantity": skus.count(sku)} for sku in set(skus)]
    
    def calculate_offer_price(self):
        pass
    
    def calculate_item_price(self, prices: list[Price], item) -> int | None:
        sku_price = next((price for price in prices if price["sku"] == item["sku"]), None)
        # Catch invalid SKU
        if not sku_price:
            return None
        
        # Check for special offer pricing including multiples
        if sku_price["special_offer"]:
            num_offers = item["quantity"] // sku_price["special_offer"]["quantity"]
            remainder = item["quantity"] % sku_price["special_offer"]["quantity"]
            return (num_offers * sku_price["special_offer"]["price"]) + (remainder * sku_price["price"])
        return sku_price["price"] * item["quantity"]

    # skus = unicode string
    def checkout(self, skus: str) -> int:
        totals = []
        prices = self.get_prices()
        item_with_quantity = self.get_item_quantity(skus)
        for item in item_with_quantity:
            totals.append(self.calculate_item_price(prices, item))
        if None in totals:
            return -1
        return sum(totals)



