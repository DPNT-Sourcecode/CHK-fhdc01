import json

from .types import Price, BulkOffer, FreeItemOffer

class CheckoutSolution:
    def __init__(self):
        self.skus: list[str] = []
        self.prices: list[Price] = self.get_prices()
        self.total: int = 0
        self.error: bool = False

    def add_to_total(self, amount: int):
        if amount is None:
            self.error = True
        self.total += amount

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
        self.skus = list(skus)
        while not self.error:
            item_with_quantity = self.get_item_quantity(skus)
            for item in item_with_quantity:
                self.add_to_total(self.calculate_item_price(prices, item))
            if None in totals:
                return -1
            return sum(totals)
        return -1
