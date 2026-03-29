"""
Pydantic schemas for product catalogue endpoints.
"""

import uuid
from decimal import Decimal

from pydantic import BaseModel


class ProductListItem(BaseModel):
    """Single product in a catalogue listing."""

    id: uuid.UUID
    name: str
    price: Decimal
    thumbnail_url: str | None
    stock_quantity: int
    stock_status: str
    category_slug: str

    model_config = {"from_attributes": True}


class CategoryResponse(BaseModel):
    """Category in a listing."""

    id: uuid.UUID
    name: str
    slug: str

    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel):
    """Paginated wrapper for product listings."""

    items: list[ProductListItem]
    total: int
    page: int
    limit: int
    has_next: bool
