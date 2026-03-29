"""
Cart service — business logic for shopping cart management.
"""

import uuid
from decimal import Decimal

import structlog

from src.models.cart import Cart
from src.repositories.cart_repository import CartRepository
from src.repositories.product_repository import ProductRepository
from src.types.cart import CartItemResponse, CartResponse

log = structlog.get_logger()

TAX_RATE = Decimal("0.10")


class CartService:
    """Business logic for cart operations."""

    def __init__(
        self,
        cart_repo: CartRepository,
        product_repo: ProductRepository,
    ) -> None:
        self._cart_repo = cart_repo
        self._product_repo = product_repo

    async def get_cart(
        self,
        *,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
    ) -> CartResponse:
        """Get the current cart with stock validation."""
        log.info("service.get_cart", user_id=str(user_id) if user_id else None)
        cart = await self._cart_repo.get_active_cart(user_id=user_id, session_id=session_id)
        if cart is None:
            return self._empty_cart()

        return self._build_cart_response(cart)

    async def add_item(
        self,
        *,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
        product_id: uuid.UUID,
        quantity: int = 1,
    ) -> CartResponse:
        """Add a product to the cart. Creates cart if needed. Increments if duplicate."""
        log.info("service.add_item", product_id=str(product_id), quantity=quantity)

        cart = await self._cart_repo.get_active_cart(user_id=user_id, session_id=session_id)
        if cart is None:
            cart = await self._cart_repo.create_cart(user_id=user_id, session_id=session_id)

        await self._cart_repo.add_item(cart_id=cart.id, product_id=product_id, quantity=quantity)

        refreshed = await self._cart_repo.get_active_cart(user_id=user_id, session_id=session_id)
        assert refreshed is not None
        return self._build_cart_response(refreshed)

    async def update_item(
        self,
        *,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
        product_id: uuid.UUID,
        quantity: int,
    ) -> CartResponse:
        """Update cart item quantity. Quantity 0 removes the item."""
        log.info("service.update_item", product_id=str(product_id), quantity=quantity)

        cart = await self._cart_repo.get_active_cart(user_id=user_id, session_id=session_id)
        if cart is None:
            return self._empty_cart()

        await self._cart_repo.update_item_quantity(
            cart_id=cart.id, product_id=product_id, quantity=quantity
        )

        refreshed = await self._cart_repo.get_active_cart(user_id=user_id, session_id=session_id)
        if refreshed is None:
            return self._empty_cart()
        return self._build_cart_response(refreshed)

    async def remove_item(
        self,
        *,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
        product_id: uuid.UUID,
    ) -> CartResponse:
        """Remove an item from the cart."""
        log.info("service.remove_item", product_id=str(product_id))

        cart = await self._cart_repo.get_active_cart(user_id=user_id, session_id=session_id)
        if cart is None:
            return self._empty_cart()

        await self._cart_repo.remove_item(cart_id=cart.id, product_id=product_id)

        refreshed = await self._cart_repo.get_active_cart(user_id=user_id, session_id=session_id)
        if refreshed is None:
            return self._empty_cart()
        return self._build_cart_response(refreshed)

    @staticmethod
    def _build_cart_response(cart: Cart) -> CartResponse:
        """Build cart response with stock validation and totals."""
        items: list[CartItemResponse] = []
        for cart_item in cart.items:
            product = cart_item.product
            quantity = cart_item.quantity
            stock_warning: str | None = None

            if product.stock_quantity < quantity:
                stock_warning = (
                    f"Only {product.stock_quantity} available. Quantity adjusted from {quantity}."
                )
                quantity = product.stock_quantity

            subtotal = product.price * quantity
            items.append(
                CartItemResponse(
                    product_id=product.id,
                    product_name=product.name,
                    price=product.price,
                    quantity=quantity,
                    subtotal=subtotal,
                    stock_warning=stock_warning,
                )
            )

        subtotal = sum((item.subtotal for item in items), Decimal("0"))
        estimated_tax = (subtotal * TAX_RATE).quantize(Decimal("0.01"))
        total = subtotal + estimated_tax
        item_count = sum(item.quantity for item in items)

        return CartResponse(
            items=items,
            subtotal=subtotal,
            estimated_tax=estimated_tax,
            total=total,
            item_count=item_count,
        )

    @staticmethod
    def _empty_cart() -> CartResponse:
        return CartResponse(
            items=[],
            subtotal=Decimal("0"),
            estimated_tax=Decimal("0"),
            total=Decimal("0"),
            item_count=0,
        )
