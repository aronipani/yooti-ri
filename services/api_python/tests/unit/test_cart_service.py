"""Unit tests for CartService.

All external dependencies (repositories) are mocked.
"""

import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.services.cart_service import CartService
from src.types.cart import CartResponse


def _make_product(
    *,
    product_id: uuid.UUID | None = None,
    price: Decimal = Decimal("29.99"),
    stock_quantity: int = 10,
    name: str = "Widget",
) -> MagicMock:
    product = MagicMock()
    product.id = product_id or uuid.uuid4()
    product.name = name
    product.price = price
    product.stock_quantity = stock_quantity
    return product


def _make_cart_item(
    *,
    product: MagicMock | None = None,
    quantity: int = 1,
) -> MagicMock:
    item = MagicMock()
    item.product = product or _make_product()
    item.quantity = quantity
    return item


def _make_cart(items: list[MagicMock] | None = None) -> MagicMock:
    cart = MagicMock()
    cart.id = uuid.uuid4()
    cart.items = items or []
    return cart


def _build_service(
    *,
    cart: MagicMock | None = None,
) -> CartService:
    cart_repo = AsyncMock()
    cart_repo.get_active_cart.return_value = cart
    cart_repo.create_cart.return_value = cart or _make_cart()
    product_repo = AsyncMock()
    return CartService(cart_repo=cart_repo, product_repo=product_repo)


class TestGetCart:
    """Tests for CartService.get_cart."""

    @pytest.mark.anyio
    async def test_returns_empty_cart_when_no_cart_exists(self) -> None:
        service = _build_service(cart=None)
        result = await service.get_cart(user_id=uuid.uuid4())
        assert isinstance(result, CartResponse)
        assert result.items == []
        assert result.item_count == 0

    @pytest.mark.anyio
    async def test_returns_items_with_correct_fields(self) -> None:
        product = _make_product(price=Decimal("10.00"))
        item = _make_cart_item(product=product, quantity=2)
        cart = _make_cart(items=[item])
        service = _build_service(cart=cart)

        result = await service.get_cart(user_id=uuid.uuid4())

        assert len(result.items) == 1
        assert result.items[0].product_name == "Widget"
        assert result.items[0].price == Decimal("10.00")
        assert result.items[0].quantity == 2
        assert result.items[0].subtotal == Decimal("20.00")

    @pytest.mark.anyio
    async def test_calculates_subtotal_correctly(self) -> None:
        p1 = _make_product(price=Decimal("10.00"))
        p2 = _make_product(price=Decimal("20.00"))
        cart = _make_cart(
            items=[
                _make_cart_item(product=p1, quantity=2),
                _make_cart_item(product=p2, quantity=1),
            ]
        )
        service = _build_service(cart=cart)

        result = await service.get_cart(user_id=uuid.uuid4())

        assert result.subtotal == Decimal("40.00")

    @pytest.mark.anyio
    async def test_calculates_estimated_tax(self) -> None:
        product = _make_product(price=Decimal("100.00"))
        cart = _make_cart(items=[_make_cart_item(product=product, quantity=1)])
        service = _build_service(cart=cart)

        result = await service.get_cart(user_id=uuid.uuid4())

        assert result.estimated_tax == Decimal("10.00")

    @pytest.mark.anyio
    async def test_stock_warning_when_quantity_exceeds_stock(self) -> None:
        product = _make_product(stock_quantity=3)
        item = _make_cart_item(product=product, quantity=5)
        cart = _make_cart(items=[item])
        service = _build_service(cart=cart)

        result = await service.get_cart(user_id=uuid.uuid4())

        assert result.items[0].stock_warning is not None
        assert "3 available" in result.items[0].stock_warning
        assert result.items[0].quantity == 3

    @pytest.mark.anyio
    async def test_no_stock_warning_when_quantity_within_stock(self) -> None:
        product = _make_product(stock_quantity=10)
        item = _make_cart_item(product=product, quantity=2)
        cart = _make_cart(items=[item])
        service = _build_service(cart=cart)

        result = await service.get_cart(user_id=uuid.uuid4())

        assert result.items[0].stock_warning is None


class TestAddItem:
    """Tests for CartService.add_item."""

    @pytest.mark.anyio
    async def test_add_item_creates_cart_if_none_exists(self) -> None:
        cart_repo = AsyncMock()
        cart_repo.get_active_cart.side_effect = [None, _make_cart()]
        cart_repo.create_cart.return_value = _make_cart()
        product_repo = AsyncMock()
        service = CartService(cart_repo=cart_repo, product_repo=product_repo)

        product_id = uuid.uuid4()
        await service.add_item(user_id=uuid.uuid4(), product_id=product_id)

        cart_repo.create_cart.assert_called_once()

    @pytest.mark.anyio
    async def test_add_item_calls_repo_with_correct_args(self) -> None:
        cart = _make_cart()
        cart_repo = AsyncMock()
        cart_repo.get_active_cart.return_value = cart
        product_repo = AsyncMock()
        service = CartService(cart_repo=cart_repo, product_repo=product_repo)

        product_id = uuid.uuid4()
        await service.add_item(user_id=uuid.uuid4(), product_id=product_id, quantity=3)

        cart_repo.add_item.assert_called_once_with(
            cart_id=cart.id, product_id=product_id, quantity=3
        )


class TestUpdateItem:
    """Tests for CartService.update_item."""

    @pytest.mark.anyio
    async def test_update_to_zero_removes_item(self) -> None:
        cart = _make_cart()
        cart_repo = AsyncMock()
        cart_repo.get_active_cart.return_value = cart
        product_repo = AsyncMock()
        service = CartService(cart_repo=cart_repo, product_repo=product_repo)

        product_id = uuid.uuid4()
        await service.update_item(user_id=uuid.uuid4(), product_id=product_id, quantity=0)

        cart_repo.update_item_quantity.assert_called_once_with(
            cart_id=cart.id, product_id=product_id, quantity=0
        )

    @pytest.mark.anyio
    async def test_returns_empty_cart_when_no_cart(self) -> None:
        cart_repo = AsyncMock()
        cart_repo.get_active_cart.return_value = None
        product_repo = AsyncMock()
        service = CartService(cart_repo=cart_repo, product_repo=product_repo)

        result = await service.update_item(
            user_id=uuid.uuid4(), product_id=uuid.uuid4(), quantity=1
        )

        assert result.items == []
