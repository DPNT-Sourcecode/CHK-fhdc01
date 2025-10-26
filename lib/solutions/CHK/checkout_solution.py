import json

from .types import RawPrice, Offer, AnalysedBasketItem

class CheckoutSolution:
    def __init__(self):
        self.items: list[str] = []
        self.prices: list[RawPrice] = self.get_prices()
        self.offers: list[Offer] = self.get_offers()
        self.total: int = 0
        self.error: bool = False
        self.basket_items: list[AnalysedBasketItem] = []

    def add_to_total(self, amount: int):
        if amount is None:
            self.error = True
        self.total += amount

    def get_prices(self) -> list[RawPrice]:
        with open("lib/solutions/CHK/prices.json") as f:
            prices: list[RawPrice] = json.load(f)
        return prices
    
    def get_offers(self) -> list[RawPrice]:
        with open("lib/solutions/CHK/offers.json") as f:
            offers: list[RawPrice] = json.load(f)
        return sorted(offers, key=lambda x: x["quantity"], reverse=True)

    def get_item_quantity(self, skus: str) -> dict[str, int]:
        return [{"sku": sku, "quantity": skus.count(sku)} for sku in set(skus)]
    
    def calculate_offer_price(self):
        pass
    
    def calculate_item_price(self, prices: list[RawPrice], item) -> int | None:
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
    
    def analyse_basket(self):
        # for item in self.items:
        pass

    # skus = unicode string
    def checkout(self, skus: str) -> int:
        self.skus = list(skus)
        while not self.error:
            self.analyse_basket()
            # item_with_quantity = self.get_item_quantity(skus)
            # for item in item_with_quantity:
            #     self.add_to_total(self.calculate_item_price(prices, item))
            # if None in totals:
            #     return -1
            # return sum(totals)
        return -1

