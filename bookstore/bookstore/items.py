# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

@dataclass
class BookstoreItem:
    # define the fields for your item here like:
    # name: str | None = None
    title: str
    price: float
    price_excl_tax: float
    price_incl_tax: float
    tax: float
    availability: int
    in_stock: bool
    rating: int
    category : str
    upc: str
    product_type: str
    num_reviews: int
    description: str
    image_url: str
    product_url: str
