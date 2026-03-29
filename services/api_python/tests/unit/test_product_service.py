"""Unit tests for ProductService.

All external dependencies (repositories) are mocked.
"""

import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.services.product_service import ProductService
from src.types.product import PaginatedResponse


def _make_category(*, slug: str = "electronics", name: str = "Electronics") -> MagicMock:
    cat = MagicMock()
    cat.id = uuid.uuid4()
    cat.name = name
    cat.slug = slug
    return cat


def _make_product(
    *,
    stock_quantity: int = 10,
    price: Decimal = Decimal("29.99"),
    category_slug: str = "electronics",
) -> MagicMock:
    product = MagicMock()
    product.id = uuid.uuid4()
    product.name = "Test Product"
    product.price = price
    product.thumbnail_url = "https://example.com/img.jpg"
    product.stock_quantity = stock_quantity
    product.category = _make_category(slug=category_slug)
    return product


def _build_service(
    *,
    products: list[MagicMock] | None = None,
    total: int = 0,
    categories: list[MagicMock] | None = None,
) -> ProductService:
    product_repo = AsyncMock()
    product_repo.list_products.return_value = (products or [], total)

    category_repo = AsyncMock()
    category_repo.list_categories.return_value = categories or []

    return ProductService(product_repo=product_repo, category_repo=category_repo)


# ===========================================================================
# list_products
# ===========================================================================


class TestListProducts:
    """Tests for ProductService.list_products."""

    @pytest.mark.anyio
    async def test_returns_paginated_response(self) -> None:
        product = _make_product()
        service = _build_service(products=[product], total=1)
        result = await service.list_products()
        assert isinstance(result, PaginatedResponse)

    @pytest.mark.anyio
    async def test_returns_correct_total(self) -> None:
        service = _build_service(products=[], total=42)
        result = await service.list_products()
        assert result.total == 42

    @pytest.mark.anyio
    async def test_maps_product_fields(self) -> None:
        product = _make_product(price=Decimal("19.99"), stock_quantity=5)
        service = _build_service(products=[product], total=1)
        result = await service.list_products()
        item = result.items[0]
        assert item.name == "Test Product"
        assert item.price == Decimal("19.99")
        assert item.stock_quantity == 5

    @pytest.mark.anyio
    async def test_in_stock_product_has_in_stock_status(self) -> None:
        product = _make_product(stock_quantity=10)
        service = _build_service(products=[product], total=1)
        result = await service.list_products()
        assert result.items[0].stock_status == "in_stock"

    @pytest.mark.anyio
    async def test_out_of_stock_product_has_out_of_stock_status(self) -> None:
        product = _make_product(stock_quantity=0)
        service = _build_service(products=[product], total=1)
        result = await service.list_products()
        assert result.items[0].stock_status == "out_of_stock"

    @pytest.mark.anyio
    async def test_has_next_true_when_more_pages(self) -> None:
        service = _build_service(products=[], total=25)
        result = await service.list_products(page=1, limit=20)
        assert result.has_next is True

    @pytest.mark.anyio
    async def test_has_next_false_on_last_page(self) -> None:
        service = _build_service(products=[], total=20)
        result = await service.list_products(page=1, limit=20)
        assert result.has_next is False

    @pytest.mark.anyio
    async def test_passes_category_filter_to_repo(self) -> None:
        product_repo = AsyncMock()
        product_repo.list_products.return_value = ([], 0)
        category_repo = AsyncMock()
        category_repo.list_categories.return_value = []
        service = ProductService(product_repo=product_repo, category_repo=category_repo)

        await service.list_products(category_slug="books")
        product_repo.list_products.assert_called_once_with(
            category_slug="books", sort=None, page=1, limit=20
        )

    @pytest.mark.anyio
    async def test_passes_sort_to_repo(self) -> None:
        product_repo = AsyncMock()
        product_repo.list_products.return_value = ([], 0)
        category_repo = AsyncMock()
        category_repo.list_categories.return_value = []
        service = ProductService(product_repo=product_repo, category_repo=category_repo)

        await service.list_products(sort="price_asc")
        product_repo.list_products.assert_called_once_with(
            category_slug=None, sort="price_asc", page=1, limit=20
        )

    @pytest.mark.anyio
    async def test_empty_result_returns_empty_items(self) -> None:
        service = _build_service(products=[], total=0)
        result = await service.list_products()
        assert result.items == []
        assert result.total == 0


# ===========================================================================
# list_categories
# ===========================================================================


class TestListCategories:
    """Tests for ProductService.list_categories."""

    @pytest.mark.anyio
    async def test_returns_list_of_category_responses(self) -> None:
        cat = _make_category()
        service = _build_service(categories=[cat])
        result = await service.list_categories()
        assert len(result) == 1
        assert result[0].slug == "electronics"

    @pytest.mark.anyio
    async def test_empty_categories(self) -> None:
        service = _build_service(categories=[])
        result = await service.list_categories()
        assert result == []
