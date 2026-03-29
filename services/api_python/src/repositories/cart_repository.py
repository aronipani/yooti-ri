"""
Cart repository — database queries for shopping carts.
"""

import uuid

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.cart import Cart, CartStatus
from src.models.cart_item import CartItem

log = structlog.get_logger()


class CartRepository:
    """Data access layer for carts."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_active_cart(
        self,
        *,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
    ) -> Cart | None:
        """Get active cart for a user or guest session."""
        log.info("repository.get_active_cart", user_id=str(user_id) if user_id else None)
        query = (
            select(Cart)
            .where(Cart.status == CartStatus.ACTIVE)
            .options(joinedload(Cart.items).joinedload(CartItem.product))
        )
        if user_id:
            query = query.where(Cart.user_id == user_id)
        elif session_id:
            query = query.where(Cart.session_id == session_id)
        else:
            return None

        result = await self._session.execute(query)
        return result.scalars().unique().first()

    async def create_cart(
        self,
        *,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
    ) -> Cart:
        """Create a new active cart."""
        log.info("repository.create_cart")
        cart = Cart(user_id=user_id, session_id=session_id)
        self._session.add(cart)
        await self._session.flush()
        return cart

    async def add_item(
        self,
        *,
        cart_id: uuid.UUID,
        product_id: uuid.UUID,
        quantity: int,
    ) -> CartItem:
        """Add or update an item in the cart."""
        log.info("repository.add_item", cart_id=str(cart_id), product_id=str(product_id))
        existing = await self._session.execute(
            select(CartItem).where(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id,
            )
        )
        item = existing.scalars().first()
        if item:
            item.quantity += quantity
        else:
            item = CartItem(
                cart_id=cart_id,
                product_id=product_id,
                quantity=quantity,
            )
            self._session.add(item)
        await self._session.flush()
        return item

    async def update_item_quantity(
        self,
        *,
        cart_id: uuid.UUID,
        product_id: uuid.UUID,
        quantity: int,
    ) -> CartItem | None:
        """Update cart item quantity. If quantity is 0, remove the item."""
        log.info("repository.update_item_quantity", product_id=str(product_id), quantity=quantity)
        result = await self._session.execute(
            select(CartItem).where(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id,
            )
        )
        item = result.scalars().first()
        if not item:
            return None

        if quantity == 0:
            await self._session.delete(item)
            await self._session.flush()
            return None

        item.quantity = quantity
        await self._session.flush()
        return item

    async def remove_item(
        self,
        *,
        cart_id: uuid.UUID,
        product_id: uuid.UUID,
    ) -> None:
        """Remove an item from the cart."""
        log.info("repository.remove_item", product_id=str(product_id))
        result = await self._session.execute(
            select(CartItem).where(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id,
            )
        )
        item = result.scalars().first()
        if item:
            await self._session.delete(item)
            await self._session.flush()
