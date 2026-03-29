"""
Unit tests for Product and Category models.
Tests verify column definitions by inspecting __table__.columns — no DB required.
"""

from src.models.base import Base
from src.models.category import Category
from src.models.product import Product

# ---------------------------------------------------------------------------
# Helper to fetch a column object from a model's __table__
# ---------------------------------------------------------------------------


def _col(model_cls: type, name: str):  # noqa: ANN202
    """Return a SQLAlchemy Column from the model's table, or raise."""
    table = model_cls.__table__
    assert name in table.columns, f"Column '{name}' not found on {table.name}"
    return table.columns[name]


# ===========================================================================
# Category model tests
# ===========================================================================


class TestCategoryModel:
    """Tests for the Category SQLAlchemy model."""

    def test_category_table_name_is_categories(self) -> None:
        assert Category.__tablename__ == "categories"

    def test_category_inherits_from_base(self) -> None:
        assert issubclass(Category, Base)

    def test_category_has_id_column(self) -> None:
        col = _col(Category, "id")
        assert col.primary_key is True

    def test_category_has_name_column(self) -> None:
        col = _col(Category, "name")
        assert col.nullable is False

    def test_category_has_slug_column(self) -> None:
        col = _col(Category, "slug")
        assert col.nullable is False

    def test_category_slug_is_unique(self) -> None:
        col = _col(Category, "slug")
        assert col.unique is True

    def test_category_has_created_at(self) -> None:
        col = _col(Category, "created_at")
        assert col.nullable is False

    def test_category_has_updated_at(self) -> None:
        col = _col(Category, "updated_at")
        assert col.nullable is False


# ===========================================================================
# Product model tests
# ===========================================================================


class TestProductModel:
    """Tests for the Product SQLAlchemy model."""

    def test_product_table_name_is_products(self) -> None:
        assert Product.__tablename__ == "products"

    def test_product_inherits_from_base(self) -> None:
        assert issubclass(Product, Base)

    def test_product_has_id_column(self) -> None:
        col = _col(Product, "id")
        assert col.primary_key is True

    def test_product_has_name_column(self) -> None:
        col = _col(Product, "name")
        assert col.nullable is False

    def test_product_has_description_column(self) -> None:
        col = _col(Product, "description")
        assert col.nullable is False

    def test_product_price_is_numeric_10_2(self) -> None:
        col = _col(Product, "price")
        assert col.nullable is False
        assert col.type.precision == 10
        assert col.type.scale == 2

    def test_product_stock_quantity_defaults_to_zero(self) -> None:
        col = _col(Product, "stock_quantity")
        assert col.nullable is False
        # server_default or default should represent 0
        assert str(col.server_default.arg) == "0"

    def test_product_is_active_defaults_to_true(self) -> None:
        col = _col(Product, "is_active")
        assert col.nullable is False
        assert str(col.server_default.arg) == "true"

    def test_product_has_category_id_fk(self) -> None:
        col = _col(Product, "category_id")
        assert col.nullable is False
        fk_targets = [fk.target_fullname for fk in col.foreign_keys]
        assert "categories.id" in fk_targets

    def test_product_thumbnail_url_is_nullable(self) -> None:
        col = _col(Product, "thumbnail_url")
        assert col.nullable is True

    def test_product_has_images_column(self) -> None:
        col = _col(Product, "images")
        assert col.nullable is False

    def test_product_has_created_at(self) -> None:
        col = _col(Product, "created_at")
        assert col.nullable is False

    def test_product_has_updated_at(self) -> None:
        col = _col(Product, "updated_at")
        assert col.nullable is False
