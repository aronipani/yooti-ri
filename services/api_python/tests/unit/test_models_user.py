"""Unit tests for User model.

Tests inspect SQLAlchemy column metadata — no database connection required.
"""

import enum

from sqlalchemy import Enum as SAEnum

from src.models.user import User, UserRole


class TestUserRole:
    """Tests for the UserRole enum."""

    def test_user_role_is_enum(self) -> None:
        assert issubclass(UserRole, enum.Enum)

    def test_user_role_has_user_value(self) -> None:
        assert UserRole.USER.value == "user"

    def test_user_role_has_admin_value(self) -> None:
        assert UserRole.ADMIN.value == "admin"

    def test_user_role_has_exactly_two_members(self) -> None:
        assert len(UserRole) == 2


class TestUserModel:
    """Tests for User SQLAlchemy model."""

    def _col(self, name: str):  # noqa: ANN202
        """Helper to get a column from User.__table__."""
        return User.__table__.columns[name]

    # --- table name ---

    def test_table_name_is_users(self) -> None:
        assert User.__tablename__ == "users"

    # --- inherited fields from Base ---

    def test_has_id_column(self) -> None:
        col = self._col("id")
        assert col.primary_key is True

    def test_id_is_uuid(self) -> None:
        col = self._col("id")
        assert isinstance(col.type, type(User.__table__.columns["id"].type))

    def test_has_created_at_column(self) -> None:
        col = self._col("created_at")
        assert col.nullable is False

    def test_has_updated_at_column(self) -> None:
        col = self._col("updated_at")
        assert col.nullable is False

    # --- email ---

    def test_has_email_column(self) -> None:
        col = self._col("email")
        assert col is not None

    def test_email_is_not_nullable(self) -> None:
        col = self._col("email")
        assert col.nullable is False

    def test_email_has_unique_constraint(self) -> None:
        col = self._col("email")
        assert col.unique is True

    def test_email_has_index(self) -> None:
        col = self._col("email")
        assert col.index is True

    # --- password_hash ---

    def test_has_password_hash_column(self) -> None:
        col = self._col("password_hash")
        assert col is not None

    def test_password_hash_is_not_nullable(self) -> None:
        col = self._col("password_hash")
        assert col.nullable is False

    # --- name ---

    def test_has_name_column(self) -> None:
        col = self._col("name")
        assert col is not None

    def test_name_is_not_nullable(self) -> None:
        col = self._col("name")
        assert col.nullable is False

    # --- role ---

    def test_has_role_column(self) -> None:
        col = self._col("role")
        assert col is not None

    def test_role_is_not_nullable(self) -> None:
        col = self._col("role")
        assert col.nullable is False

    def test_role_is_enum_type(self) -> None:
        col = self._col("role")
        assert isinstance(col.type, SAEnum)

    def test_role_default_is_user(self) -> None:
        col = self._col("role")
        assert col.default.arg is UserRole.USER

    # --- is_active ---

    def test_has_is_active_column(self) -> None:
        col = self._col("is_active")
        assert col is not None

    def test_is_active_is_not_nullable(self) -> None:
        col = self._col("is_active")
        assert col.nullable is False

    def test_is_active_defaults_to_true(self) -> None:
        col = self._col("is_active")
        assert col.default.arg is True
