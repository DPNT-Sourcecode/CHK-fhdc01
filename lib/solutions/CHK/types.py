from typing import TypedDict


class BulkOffer(TypedDict):
    sku: str
    quantity: int
    price: int

class FreeItemOffer(TypedDict):
    sku: str
    quantity: int
    free_sku: str
    free_quantity: int

class RawPrice(TypedDict):
    sku: str
    price: int

class Offers(TypedDict):
    bulk_buys: list[BulkOffer]
    free_item_offers: list[FreeItemOffer]

class AnalysedBasketItem(TypedDict):
    sku: str
    quantity: int
    price: int
    adjusted_price: int



