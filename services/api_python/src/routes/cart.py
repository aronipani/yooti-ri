"""
Cart routes.
Thin controllers: validate input, call service, return response.
"""

import uuid

import structlog
from fastapi import APIRouter, Cookie, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.middleware.auth import require_auth
from src.models.user import User
from src.repositories.cart_repository import CartRepository
from src.repositories.product_repository import ProductRepository
from src.services.cart_service import CartService
from src.types.cart import AddToCartRequest, CartResponse, UpdateCartItemRequest

log = structlog.get_logger()

router = APIRouter(prefix="/api/v1/cart", tags=["cart"])


def _get_cart_service(session: AsyncSession = Depends(get_db)) -> CartService:
    return CartService(
        cart_repo=CartRepository(session),
        product_repo=ProductRepository(session),
    )


@router.get("", response_model=CartResponse)
async def get_cart(
    current_user: User | None = Depends(require_auth),
    session_id: str | None = Cookie(None, alias="cart_session_id"),
    service: CartService = Depends(_get_cart_service),
) -> CartResponse:
    """Get the current cart."""
    log.info("route.get_cart")
    user_id = current_user.id if current_user else None
    return await service.get_cart(user_id=user_id, session_id=session_id)


@router.post("/items", response_model=CartResponse, status_code=201)
async def add_to_cart(
    body: AddToCartRequest,
    current_user: User | None = Depends(require_auth),
    session_id: str | None = Cookie(None, alias="cart_session_id"),
    service: CartService = Depends(_get_cart_service),
) -> CartResponse:
    """Add a product to the cart."""
    log.info("route.add_to_cart", product_id=str(body.product_id))
    user_id = current_user.id if current_user else None
    return await service.add_item(
        user_id=user_id,
        session_id=session_id,
        product_id=body.product_id,
        quantity=body.quantity,
    )


@router.put("/items/{product_id}", response_model=CartResponse)
async def update_cart_item(
    body: UpdateCartItemRequest,
    product_id: uuid.UUID = Path(description="Product UUID"),
    current_user: User | None = Depends(require_auth),
    session_id: str | None = Cookie(None, alias="cart_session_id"),
    service: CartService = Depends(_get_cart_service),
) -> CartResponse:
    """Update the quantity of a cart item. Quantity 0 removes it."""
    log.info("route.update_cart_item", product_id=str(product_id), quantity=body.quantity)
    user_id = current_user.id if current_user else None
    return await service.update_item(
        user_id=user_id,
        session_id=session_id,
        product_id=product_id,
        quantity=body.quantity,
    )


@router.delete("/items/{product_id}", response_model=CartResponse)
async def remove_cart_item(
    product_id: uuid.UUID = Path(description="Product UUID"),
    current_user: User | None = Depends(require_auth),
    session_id: str | None = Cookie(None, alias="cart_session_id"),
    service: CartService = Depends(_get_cart_service),
) -> CartResponse:
    """Remove a product from the cart."""
    log.info("route.remove_cart_item", product_id=str(product_id))
    user_id = current_user.id if current_user else None
    return await service.remove_item(
        user_id=user_id,
        session_id=session_id,
        product_id=product_id,
    )
