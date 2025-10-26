from typing import TypedDict


class BulkOffer(TypedDict):
    type = "bulk"
    quantity: int
    price: int

class FreeItemOffer(TypedDict):
    type = "free_item"
    quantity: int
    free_sku: str
    free_quantity: int

class Price(TypedDict):
    sku: str
    price: int



