"""
Product repository — database queries for products and categories.
"""

import uuid
from collections.abc import Sequence

import structlog
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.category import Category
from src.models.product import Product

log = structlog.get_logger()


class ProductRepository:
    """Data access layer for products."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_products(
        self,
        *,
        category_slug: str | None = None,
        sort: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[Sequence[Product], int]:
        """Return paginated, filtered, sorted active products and total count."""
        log.info(
            "repository.list_products",
            category_slug=category_slug,
            sort=sort,
            page=page,
            limit=limit,
        )

        base: Select[tuple[Product]] = (
            select(Product).where(Product.is_active.is_(True)).options(joinedload(Product.category))
        )

        count_q = select(func.count()).select_from(Product).where(Product.is_active.is_(True))

        if category_slug:
            base = base.join(Category).where(Category.slug == category_slug)
            count_q = count_q.join(Category).where(Category.slug == category_slug)

        if sort == "price_asc":
            base = base.order_by(Product.price.asc())
        elif sort == "price_desc":
            base = base.order_by(Product.price.desc())
        else:
            base = base.order_by(Product.created_at.desc())

        offset = (page - 1) * limit
        query = base.offset(offset).limit(limit)

        result = await self._session.execute(query)
        products = result.scalars().unique().all()

        count_result = await self._session.execute(count_q)
        total = count_result.scalar_one()

        return products, total

    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        """Return a single product by ID with its category loaded, or None."""
        log.info("repository.get_by_id", product_id=str(product_id))
        result = await self._session.execute(
            select(Product)
            .where(Product.id == product_id, Product.is_active.is_(True))
            .options(joinedload(Product.category))
        )
        return result.scalars().first()


class CategoryRepository:
    """Data access layer for categories."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_categories(self) -> Sequence[Category]:
        """Return all categories ordered by name."""
        log.info("repository.list_categories")
        result = await self._session.execute(select(Category).order_by(Category.name))
        return result.scalars().all()
