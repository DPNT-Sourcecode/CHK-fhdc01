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

    def get_prices(self) -> list[RawPrice]:
        with open("lib/solutions/CHK/prices.json") as f:
            prices: list[RawPrice] = json.load(f)
        return prices
    
    def get_offers(self) -> list[RawPrice]:
        with open("lib/solutions/CHK/offers.json") as f:
            offers: list[RawPrice] = json.load(f)
        # Prioritise offers with higher quantity first
        return sorted(offers, key=lambda x: x["quantity"], reverse=True)

    def clear_basket(self) -> NoReturn:
        self.items = []
        self.total = 0
        self.error = False
        self.basket_items = []
        self.basket_items_offer_applied = []

    def quantify_basket(self) -> NoReturn:
        for sku in set(self.items):
            quantity = self.items.count(sku)
            item: BasketItem = {
                "sku": sku,
                "quantity": quantity,
                "adjusted_price": None,
                "offer_applied": False
            }
            self.basket_items.append(item)
        self.basket_items.sort(key=lambda x: x["quantity"], reverse=True)

    def apply_offers(self) -> NoReturn:
        for item in self.basket_items:
            applicable_offers = [offer for offer in self.offers if offer["sku"] == item["sku"]]
            if applicable_offers:
                # sort applicable offers by quantity descending
                applicable_offers.sort(key=lambda x: x["quantity"], reverse=True)
                for offer in applicable_offers:
                    if offer["offer_type"] == "bulk_buy":
                        self.apply_bulk_buy_offer(offer)
                    if offer["offer_type"] == "free_item":
                        self.apply_free_item_offer(offer)

    # skus = unicode string
    def checkout(self, skus: str) -> int:
        # Testing framework may be reusing the same instance, so clear previous state
        self.clear_basket()
        try:
            self.items = list(skus)
            self.quantify_basket()
            self.apply_offers()
            self.process_remaining_items()
            self.calculate_total()
            return self.total
        except ValueError as e:
            print(e)
            return -1

