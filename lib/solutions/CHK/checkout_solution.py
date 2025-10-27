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
                free_item = next((item for item in self.basket_items if item["sku"] == offer["free_sku"]), None)
                if free_item:
                    if offer["free_quantity"] >= free_item["quantity"]:
                        # all free items are free as the basket has less or equal free items than the offer provides
                        analysed_item: AnalysedBasketItem = {
                            "sku": item["sku"],
                            "quantity": free_item["quantity"],
                            "adjusted_price": 0
                        }
                    else:
                        # only some of the free items are free as the basket has more free items than the offer provides
                        adjusted_price = (item["quantity"] * self.get_item_price(item["sku"])) - \
                            (offer["free_quantity"] * self.get_item_price(free_item["sku"]))
                        analysed_item: AnalysedBasketItem = {
                            "sku": item["sku"],
                            "quantity": item["quantity"],
                            "adjusted_price": adjusted_price
                        }
                    self.basket_items.remove(item)
                    self.basket_items_offer_applied.append(analysed_item)
                else:
                    # free item not in basket, add it with adjusted price of 0
                    analysed_item: AnalysedBasketItem = {
                        "sku": offer["sku"],
                        "quantity": offer["quantity"],
                        "adjusted_price": 0
                    }
                    self.basket_items_offer_applied.append(analysed_item)

    def apply_offers(self) -> NoReturn:
        for offer in self.offers: # offers should already be prioritised by quantity
            if offer["offer_type"] == "bulk_buy":
                self.apply_bulk_buy_offer(offer)
            if offer["offer_type"] == "free_item":
                self.apply_free_item_offer(offer)

    def process_remaining_items(self) -> NoReturn:
        for item in self.basket_items:
            adjusted_price = item["quantity"] * self.get_item_price(item["sku"])
            analysed_item: AnalysedBasketItem = {
                "sku": item["sku"],
                "quantity": item["quantity"],
                "adjusted_price": adjusted_price
            }
            self.basket_items.remove(item)
            self.basket_items_offer_applied.append(analysed_item)

    def calculate_total(self) -> NoReturn:
        for item in self.basket_items_offer_applied:
            self.total += item["adjusted_price"]

    # skus = unicode string
    def checkout(self, skus: str) -> int:
        self.items = list(skus)
        print("==================================")
        print(self.items)
        while not self.error:
            self.quantify_basket() # Get quantity of each item in the basket
            print( self.basket_items)
            self.apply_offers() # Apply offers, prioritise offers with higher quantity first
            print( self.basket_items)
            print(self.basket_items_offer_applied)
            self.process_remaining_items() # Process any remaining items without offers
            print(self.basket_items_offer_applied)
            print("==================================")
            self.calculate_total() # Calculate total price using adjusted prices
            return self.total
        return -1



