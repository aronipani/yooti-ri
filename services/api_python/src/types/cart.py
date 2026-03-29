"""
Pydantic schemas for cart endpoints.
"""

import uuid
from decimal import Decimal

from pydantic import BaseModel, Field


class AddToCartRequest(BaseModel):
    """Request to add a product to the cart."""

    product_id: uuid.UUID
    quantity: int = Field(ge=1, default=1)


class UpdateCartItemRequest(BaseModel):
    """Request to update cart item quantity."""

    quantity: int = Field(ge=0)


class CartItemResponse(BaseModel):
    """Single cart item in the response."""

    product_id: uuid.UUID
    product_name: str
    price: Decimal
    quantity: int
    subtotal: Decimal
    stock_warning: str | None = None

    model_config = {"from_attributes": True}


class CartResponse(BaseModel):
    """Full cart response."""

    items: list[CartItemResponse]
    subtotal: Decimal
    estimated_tax: Decimal
    total: Decimal
    item_count: int
