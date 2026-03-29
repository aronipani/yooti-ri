"""Unit tests for Cart and CartItem models.

Tests inspect SQLAlchemy column metadata — no database connection required.
"""

from src.models.base import Base
from src.models.cart import Cart
from src.models.cart_item import CartItem


def _col(model_cls: type, name: str):  # noqa: ANN202
    """Return a SQLAlchemy Column from the model's table, or raise."""
    table = model_cls.__table__
    assert name in table.columns, f"Column '{name}' not found on {table.name}"
    return table.columns[name]


# ===========================================================================
# Cart model tests
# ===========================================================================


class TestCartModel:
    """Tests for the Cart SQLAlchemy model."""

    def test_cart_table_name_is_carts(self) -> None:
        assert Cart.__tablename__ == "carts"

    def test_cart_inherits_from_base(self) -> None:
        assert issubclass(Cart, Base)

    def test_cart_has_id_column(self) -> None:
        col = _col(Cart, "id")
        assert col.primary_key is True

    def test_cart_has_user_id_fk(self) -> None:
        col = _col(Cart, "user_id")
        fk_targets = [fk.target_fullname for fk in col.foreign_keys]
        assert "users.id" in fk_targets

    def test_cart_user_id_is_nullable(self) -> None:
        col = _col(Cart, "user_id")
        assert col.nullable is True

    def test_cart_has_session_id_column(self) -> None:
        col = _col(Cart, "session_id")
        assert col is not None

    def test_cart_session_id_is_nullable(self) -> None:
        col = _col(Cart, "session_id")
        assert col.nullable is True

    def test_cart_has_status_column(self) -> None:
        col = _col(Cart, "status")
        assert col.nullable is False

    def test_cart_has_created_at(self) -> None:
        col = _col(Cart, "created_at")
        assert col.nullable is False

    def test_cart_has_updated_at(self) -> None:
        col = _col(Cart, "updated_at")
        assert col.nullable is False


# ===========================================================================
# CartItem model tests
# ===========================================================================


class TestCartItemModel:
    """Tests for the CartItem SQLAlchemy model."""

    def test_cart_item_table_name_is_cart_items(self) -> None:
        assert CartItem.__tablename__ == "cart_items"

    def test_cart_item_inherits_from_base(self) -> None:
        assert issubclass(CartItem, Base)

    def test_cart_item_has_id_column(self) -> None:
        col = _col(CartItem, "id")
        assert col.primary_key is True

    def test_cart_item_has_cart_id_fk(self) -> None:
        col = _col(CartItem, "cart_id")
        assert col.nullable is False
        fk_targets = [fk.target_fullname for fk in col.foreign_keys]
        assert "carts.id" in fk_targets

    def test_cart_item_has_product_id_fk(self) -> None:
        col = _col(CartItem, "product_id")
        assert col.nullable is False
        fk_targets = [fk.target_fullname for fk in col.foreign_keys]
        assert "products.id" in fk_targets

    def test_cart_item_has_quantity_column(self) -> None:
        col = _col(CartItem, "quantity")
        assert col.nullable is False

    def test_cart_item_has_unique_constraint_on_cart_product(self) -> None:
        """Cart + product pair must be unique (no duplicate line items)."""
        table = CartItem.__table__
        unique_constraints = [
            c for c in table.constraints if hasattr(c, "columns") and len(c.columns) > 1
        ]
        col_names_sets = [{col.name for col in c.columns} for c in unique_constraints]
        assert {"cart_id", "product_id"} in col_names_sets

    def test_cart_item_has_created_at(self) -> None:
        col = _col(CartItem, "created_at")
        assert col.nullable is False

    def test_cart_item_has_updated_at(self) -> None:
        col = _col(CartItem, "updated_at")
        assert col.nullable is False
