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
                "adjusted_price": None,
                "offer_applied": False
            }
            self.basket_items.append(item)
        self.basket_items.sort(key=lambda x: x["sku"], reverse=True)

    def get_item_price(self, sku: str) -> int | None:
        sku_price = next((price for price in self.prices if price["sku"] == sku), None)
        if not sku_price:
            raise ValueError()
        return sku_price["price"]
    
    def update_raw_basket(self, sku: str, remove_quantity: int) -> NoReturn:
        item = next((item for item in self.basket_items if item["sku"] == sku), None)
        if item:
            item["quantity"] -= remove_quantity
            self.basket_items = [i for i in self.basket_items if i['sku'] != sku]
            self.basket_items.append(item)

    def apply_bulk_buy_offer(self, offer: Offer, item: BasketItem) -> NoReturn:
        if item["sku"] == offer["sku"] and item["quantity"] >= offer["quantity"]:
            adjusted_price = offer["price"]
            analysed_item: AnalysedBasketItem = {
                "sku": item["sku"],
                "quantity": offer["quantity"],
                "adjusted_price": adjusted_price,
                "offer_applied": True
            }
            self.update_raw_basket(item["sku"], offer["quantity"])
            self.basket_items_offer_applied.append(analysed_item)

    def apply_free_item_offer(self, offer: Offer, item: BasketItem) -> NoReturn:
        if item["sku"] == offer["sku"] and item["quantity"] >= offer["quantity"]:
            # check if the free item is in the basket already
            free_item = next((item for item in self.basket_items if item["sku"] == offer["free_sku"]), None)
            if not free_item:
                free_item = next((item for item in self.basket_items_offer_applied if item["sku"] == offer["free_sku"]), None)
            if free_item['sku'] == offer["free_sku"]:
                analysed_item: AnalysedBasketItem = {
                        "sku": free_item["sku"],
                        "quantity": offer["free_quantity"],
                        "adjusted_price": 0,
                        "offer_applied": True
                    }
                self.update_raw_basket(offer["free_sku"], offer["free_quantity"])
                self.basket_items_offer_applied.append(analysed_item)
            elif free_item and not free_item["offer_applied"]:
                if offer["free_quantity"] >= free_item["quantity"]:
                    # all free items are free as the basket has less or equal free items than the offer provides
                    analysed_item: AnalysedBasketItem = {
                        "sku": free_item["sku"],
                        "quantity": free_item["quantity"],
                        "adjusted_price": 0,
                        "offer_applied": True
                    }
                else:
                    analysed_item: AnalysedBasketItem = {
                        "sku": free_item["sku"],
                        "quantity": free_item["quantity"],
                        "adjusted_price": 0,
                        "offer_applied": True
                    }
                self.update_raw_basket(offer["free_sku"], offer["free_quantity"])
                self.basket_items_offer_applied.append(analysed_item)
            elif free_item and free_item["offer_applied"]:
                # free item already had an offer applied, do nothing
                pass
            else:
                # free item not in basket, add it with adjusted price of 0
                analysed_item: AnalysedBasketItem = {
                    "sku": offer["sku"],
                    "quantity": offer["quantity"],
                    "adjusted_price": 0,
                    "offer_applied": True
                }
                self.basket_items_offer_applied.append(analysed_item)

    def apply_offers(self) -> NoReturn:
        for item in self.basket_items:
            applicable_offers = [offer for offer in self.offers if offer["sku"] == item["sku"]]
            if applicable_offers:
                # sort applicable offers by quantity descending
                applicable_offers.sort(key=lambda x: x["quantity"], reverse=True)
                for offer in applicable_offers:
                    if offer["offer_type"] == "bulk_buy":
                        number_of_offers = item["quantity"] // offer["quantity"]
                        for _ in range(number_of_offers):
                            self.apply_bulk_buy_offer(offer, item)
                    if offer["offer_type"] == "free_item":
                        number_of_offers = item["quantity"] // offer["quantity"]
                        for _ in range(number_of_offers):
                            self.apply_free_item_offer(offer, item)

    def process_remaining_items(self) -> NoReturn:
        for item in self.basket_items:
            adjusted_price = item["quantity"] * self.get_item_price(item["sku"])
            analysed_item: AnalysedBasketItem = {
                "sku": item["sku"],
                "quantity": item["quantity"],
                "adjusted_price": adjusted_price,
                "offer_applied": False
            }
            self.basket_items_offer_applied.append(analysed_item)

    def calculate_total(self) -> NoReturn:
        for item in self.basket_items_offer_applied:
            self.total += item["adjusted_price"]

    def clear_basket(self) -> NoReturn:
        self.items = []
        self.total = 0
        self.error = False
        self.basket_items = []
        self.basket_items_offer_applied = []

    # skus = unicode string
    def checkout(self, skus: str) -> int:
        # Testing framework may be reusing the same instance, so clear previous state
        self.clear_basket()
        try:
            self.items = list(skus)
            self.quantify_basket() # Get quantity of each item in the basket
            self.apply_offers() # Apply offers, prioritise offers with higher quantity first
            self.process_remaining_items() # Process any remaining items without offers
            self.calculate_total() # Calculate total price using adjusted prices
            return self.total
        except ValueError as e:
            print(e)
            return -1



