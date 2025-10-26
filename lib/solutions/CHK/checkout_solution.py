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

    def quantify_basket(self) -> NoReturn:
        for sku in set(self.items):
            quantity = self.items.count(sku)
            item: BasketItem = {
                "sku": sku,
                "quantity": quantity,
                "adjusted_price": None
            }
            self.basket_items.append(item)

    def get_item_price(self, sku: str) -> int | None:
        sku_price = next((price for price in self.prices if price["sku"] == sku), None)
        if not sku_price:
            self.error = True
            return
        return sku_price["price"]

    def apply_bulk_buy_offer(self, offer: Offer) -> NoReturn:
        for item in self.basket_items:
            if item["sku"] == offer["sku"] and item["quantity"] >= offer["quantity"]:
                num_offers = item["quantity"] // offer["quantity"]
                remainder = item["quantity"] % offer["quantity"]
                adjusted_price = (num_offers * offer["price"]) + (remainder * self.get_item_price(item["sku"]))
                analysed_item: AnalysedBasketItem = {
                    "sku": item["sku"],
                    "quantity": item["quantity"],
                    "adjusted_price": adjusted_price
                }
                self.basket_items.remove(item)
                self.basket_items_offer_applied.append(analysed_item)

    def apply_free_item_offer(self, offer: Offer) -> NoReturn:
        for item in self.basket_items:
            if item["sku"] == offer["sku"] and item["quantity"] >= offer["quantity"]:
                # check if the free item is in the basket already
                # subtract the price of the free quantity from it
                free_item = next((item for item in self.basket_items if item["sku"] == offer["free_sku"]), None)
                if free_item:
                    adjusted_price = (item["quantity"] * self.get_item_price(item["sku"])) - \
                          (offer["free_quantity"] * self.get_item_price(free_item["sku"]))
                    analysed_item: AnalysedBasketItem = {
                        "sku": item["sku"],
                        "quantity": item["quantity"],
                        "adjusted_price": adjusted_price
                    }
                    self.basket_items.remove(item)
                    self.basket_items_offer_applied.append(analysed_item)

    def apply_offers(self) -> NoReturn:
        for offer in self.offers: # offers should already be prioritised by quantity
            if offer["offer_type"] == "bulk_buy":
                self.apply_bulk_buy_offer(offer)
            if offer["offer_type"] == "free_item":
                pass

    # skus = unicode string
    def checkout(self, skus: str) -> int:
        self.items = list(skus)
        while not self.error:
            self.quantify_basket() # Get quantity of each item in the basket
            # Apply offers, prioritise offers with higher quantity first
            # the adjusted price should be added to the item in the basket
            # Calculate total price using adjusted prices
        return -1






