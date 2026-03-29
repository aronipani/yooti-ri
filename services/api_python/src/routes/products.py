"""
Product catalogue routes.
Thin controllers: validate params, call service, return response.
"""

import uuid

import structlog
from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.errors import NotFoundError
from src.repositories.product_repository import CategoryRepository, ProductRepository
from src.services.product_service import ProductService
from src.types.product import CategoryResponse, PaginatedResponse
from src.types.product_detail import ProductDetailResponse

log = structlog.get_logger()

router = APIRouter(prefix="/api/v1", tags=["products"])


def _get_product_service(session: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(
        product_repo=ProductRepository(session),
        category_repo=CategoryRepository(session),
    )


@router.get("/products", response_model=PaginatedResponse)
async def list_products(
    category: str | None = Query(None, description="Filter by category slug"),
    sort: str | None = Query(None, description="Sort order: price_asc, price_desc"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    service: ProductService = Depends(_get_product_service),
) -> PaginatedResponse:
    """List products with optional filtering, sorting, and pagination."""
    log.info("route.list_products", category=category, sort=sort, page=page, limit=limit)
    return await service.list_products(category_slug=category, sort=sort, page=page, limit=limit)


@router.get("/products/{product_id}", response_model=ProductDetailResponse)
async def get_product_detail(
    product_id: uuid.UUID = Path(description="Product UUID"),
    service: ProductService = Depends(_get_product_service),
) -> ProductDetailResponse | JSONResponse:
    """Get full product detail by UUID."""
    log.info("route.get_product_detail", product_id=str(product_id))
    try:
        return await service.get_product_detail(product_id=product_id)
    except NotFoundError as err:
        return JSONResponse(
            status_code=err.status_code,
            content={"detail": err.message},
        )


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(
    service: ProductService = Depends(_get_product_service),
) -> list[CategoryResponse]:
    """List all product categories."""
    log.info("route.list_categories")
    return await service.list_categories()
