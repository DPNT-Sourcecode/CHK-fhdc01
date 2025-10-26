from typing import TypedDict, Union

class BulkOffer(TypedDict):
    offer_type: str
    sku: str
    quantity: int
    price: int

class FreeItemOffer(TypedDict):
    offer_type: str
    sku: str
    quantity: int
    free_sku: str
    free_quantity: int

class Offer(TypedDict):
    __root__: Union[BulkOffer, FreeItemOffer]

class RawPrice(TypedDict):
    sku: str
    price: int

class BasketItem(TypedDict):
    sku: str
    quantity: int

class AnalysedBasketItem(TypedDict):
    sku: str
    quantity: int
    adjusted_price: int
