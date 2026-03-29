"""
Cart model — shopping cart for authenticated and guest users.
"""

from __future__ import annotations

import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .cart_item import CartItem
    from .user import User


class CartStatus(enum.Enum):
    """Cart lifecycle states."""

    ACTIVE = "active"
    CHECKED_OUT = "checked_out"
    ABANDONED = "abandoned"


class Cart(Base):
    """Shopping cart for a user or guest session."""

    __tablename__ = "carts"

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    session_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[CartStatus] = mapped_column(
        Enum(CartStatus, name="cartstatus", native_enum=True),
        nullable=False,
        default=CartStatus.ACTIVE,
    )

    # Relationships
    user: Mapped[User | None] = relationship("User")
    items: Mapped[list[CartItem]] = relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )
