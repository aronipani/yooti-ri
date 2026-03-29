"""
Pydantic schemas for product detail endpoint.
"""

import uuid
from decimal import Decimal

from pydantic import BaseModel


class ProductDetailResponse(BaseModel):
    """Full product detail response."""

    id: uuid.UUID
    name: str
    description: str
    price: Decimal
    stock_quantity: int
    stock_status: str
    thumbnail_url: str | None
    images: list[str]
    category_name: str
    category_slug: str

    model_config = {"from_attributes": True}
