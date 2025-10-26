import json
from typing import NoReturn

from .types import RawPrice, Offer, AnalysedBasketItem, BasketItem

class CheckoutSolution:
    def __init__(self):
        self.items: list[str] = []
        self.prices: list[RawPrice] = self.get_prices()
        self.offers: list[Offer] = self.get_offers()
        self.total: int = 0
        self.error: bool = False
        self.basket_items: list[BasketItem] = []
        self.basket_items_offer_applied: list[AnalysedBasketItem] = []

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
        # Prioritise offers with higher quantity first
        return sorted(offers, key=lambda x: x["quantity"], reverse=True)

    def quantify_basket(self) -> NoReturn:
        for sku in set(self.items):
            quantity = self.items.count(sku)
            item: BasketItem = {
                "sku": sku,
                "quantity": quantity,
                "adjusted_price": None
            }
            self.basket_items.append(item)

    def apply_bulk_buy_offer(self, offer: Offer) -> NoReturn:
        for item in self.basket_items:
            if item["sku"] == offer["sku"] and item["quantity"] >= offer["quantity"]:
                num_offers = item["quantity"] // offer["quantity"]
                remainder = item["quantity"] % offer["quantity"]
                adjusted_price = (num_offers * offer["price"]) + (remainder * self.calculate_item_price(self.prices, item))
                analysed_item: AnalysedBasketItem = {
                    "sku": item["sku"],
                    "quantity": item["quantity"],
                    "adjusted_price": adjusted_price
                }
                self.basket_items_offer_applied.append(analysed_item)

    def apply_offers(self) -> NoReturn:
        for offer in self.offers:
            if offer["offer_type"] == "bulk_buy":
                self.apply_bulk_buy_offer(offer)
        
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

    # skus = unicode string
    def checkout(self, skus: str) -> int:
        self.items = list(skus)
        while not self.error:
            self.quantify_basket() # Get quantity of each item in the basket
            # Apply offers, prioritise offers with higher quantity first
            # the adjusted price should be added to the item in the basket
            # Calculate total price using adjusted prices
        return -1

