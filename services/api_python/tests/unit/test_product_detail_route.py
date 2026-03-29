"""Unit tests for product detail service and route.

All external dependencies (repositories) are mocked.
"""

import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.errors import NotFoundError
from src.services.product_service import ProductService


def _make_category(*, slug: str = "electronics", name: str = "Electronics") -> MagicMock:
    cat = MagicMock()
    cat.id = uuid.uuid4()
    cat.name = name
    cat.slug = slug
    return cat


def _make_product(
    *,
    product_id: uuid.UUID | None = None,
    stock_quantity: int = 10,
) -> MagicMock:
    product = MagicMock()
    product.id = product_id or uuid.uuid4()
    product.name = "Widget"
    product.description = "A fine widget"
    product.price = Decimal("49.99")
    product.stock_quantity = stock_quantity
    product.thumbnail_url = "https://example.com/widget.jpg"
    product.images = ["https://example.com/widget-1.jpg"]
    product.category = _make_category()
    return product


class TestGetProductDetail:
    """Tests for ProductService.get_product_detail."""

    @pytest.mark.anyio
    async def test_returns_product_detail_for_valid_uuid(self) -> None:
        product = _make_product()
        product_repo = AsyncMock()
        product_repo.get_by_id.return_value = product
        category_repo = AsyncMock()

        service = ProductService(product_repo=product_repo, category_repo=category_repo)
        result = await service.get_product_detail(product_id=product.id)

        assert result.name == "Widget"
        assert result.description == "A fine widget"
        assert result.price == Decimal("49.99")

    @pytest.mark.anyio
    async def test_returns_all_images(self) -> None:
        product = _make_product()
        product_repo = AsyncMock()
        product_repo.get_by_id.return_value = product
        category_repo = AsyncMock()

        service = ProductService(product_repo=product_repo, category_repo=category_repo)
        result = await service.get_product_detail(product_id=product.id)

        assert result.images == ["https://example.com/widget-1.jpg"]

    @pytest.mark.anyio
    async def test_returns_category_info(self) -> None:
        product = _make_product()
        product_repo = AsyncMock()
        product_repo.get_by_id.return_value = product
        category_repo = AsyncMock()

        service = ProductService(product_repo=product_repo, category_repo=category_repo)
        result = await service.get_product_detail(product_id=product.id)

        assert result.category_name == "Electronics"
        assert result.category_slug == "electronics"

    @pytest.mark.anyio
    async def test_in_stock_product_has_in_stock_status(self) -> None:
        product = _make_product(stock_quantity=5)
        product_repo = AsyncMock()
        product_repo.get_by_id.return_value = product
        category_repo = AsyncMock()

        service = ProductService(product_repo=product_repo, category_repo=category_repo)
        result = await service.get_product_detail(product_id=product.id)

        assert result.stock_status == "in_stock"

    @pytest.mark.anyio
    async def test_out_of_stock_product_has_out_of_stock_status(self) -> None:
        product = _make_product(stock_quantity=0)
        product_repo = AsyncMock()
        product_repo.get_by_id.return_value = product
        category_repo = AsyncMock()

        service = ProductService(product_repo=product_repo, category_repo=category_repo)
        result = await service.get_product_detail(product_id=product.id)

        assert result.stock_status == "out_of_stock"

    @pytest.mark.anyio
    async def test_raises_not_found_for_missing_product(self) -> None:
        product_repo = AsyncMock()
        product_repo.get_by_id.return_value = None
        category_repo = AsyncMock()

        service = ProductService(product_repo=product_repo, category_repo=category_repo)
        missing_id = uuid.uuid4()

        with pytest.raises(NotFoundError) as exc_info:
            await service.get_product_detail(product_id=missing_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.resource == "Product"
