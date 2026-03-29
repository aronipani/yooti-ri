"""
Product service — business logic for the product catalogue.
"""

import uuid

import structlog

from src.errors import NotFoundError
from src.models.product import Product
from src.repositories.product_repository import CategoryRepository, ProductRepository
from src.types.product import (
    CategoryResponse,
    PaginatedResponse,
    ProductListItem,
)
from src.types.product_detail import ProductDetailResponse

log = structlog.get_logger()


class ProductService:
    """Business logic for browsing the product catalogue."""

    def __init__(
        self,
        product_repo: ProductRepository,
        category_repo: CategoryRepository,
    ) -> None:
        self._product_repo = product_repo
        self._category_repo = category_repo

    async def list_products(
        self,
        *,
        category_slug: str | None = None,
        sort: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse:
        """Return paginated product list with filters and sorting."""
        log.info(
            "service.list_products",
            category_slug=category_slug,
            sort=sort,
            page=page,
            limit=limit,
        )

        products, total = await self._product_repo.list_products(
            category_slug=category_slug,
            sort=sort,
            page=page,
            limit=limit,
        )

        items = [self._to_list_item(p) for p in products]
        has_next = (page * limit) < total

        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            limit=limit,
            has_next=has_next,
        )

    async def get_product_detail(self, *, product_id: uuid.UUID) -> ProductDetailResponse:
        """Return full product detail or raise NotFoundError."""
        log.info("service.get_product_detail", product_id=str(product_id))
        product = await self._product_repo.get_by_id(product_id)
        if product is None:
            raise NotFoundError("Product", str(product_id))

        stock_status = "in_stock" if product.stock_quantity > 0 else "out_of_stock"
        return ProductDetailResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock_quantity=product.stock_quantity,
            stock_status=stock_status,
            thumbnail_url=product.thumbnail_url,
            images=product.images,
            category_name=product.category.name,
            category_slug=product.category.slug,
        )

    async def list_categories(self) -> list[CategoryResponse]:
        """Return all categories."""
        log.info("service.list_categories")
        categories = await self._category_repo.list_categories()
        return [CategoryResponse(id=c.id, name=c.name, slug=c.slug) for c in categories]

    @staticmethod
    def _to_list_item(product: Product) -> ProductListItem:
        """Map a Product ORM object to a ProductListItem schema."""
        stock_status = "in_stock" if product.stock_quantity > 0 else "out_of_stock"
        return ProductListItem(
            id=product.id,
            name=product.name,
            price=product.price,
            thumbnail_url=product.thumbnail_url,
            stock_quantity=product.stock_quantity,
            stock_status=stock_status,
            category_slug=product.category.slug,
        )
