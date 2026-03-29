"""Unit tests for Session model and User lockout fields.

Tests inspect SQLAlchemy column metadata — no database connection required.
"""

from src.models.base import Base
from src.models.session import Session
from src.models.user import User


def _col(model_cls: type, name: str):  # noqa: ANN202
    """Return a SQLAlchemy Column from the model's table, or raise."""
    table = model_cls.__table__
    assert name in table.columns, f"Column '{name}' not found on {table.name}"
    return table.columns[name]


# ===========================================================================
# Session model tests
# ===========================================================================


class TestSessionModel:
    """Tests for the Session SQLAlchemy model."""

    def test_session_table_name_is_sessions(self) -> None:
        assert Session.__tablename__ == "sessions"

    def test_session_inherits_from_base(self) -> None:
        assert issubclass(Session, Base)

    def test_session_has_id_column(self) -> None:
        col = _col(Session, "id")
        assert col.primary_key is True

    def test_session_has_user_id_fk(self) -> None:
        col = _col(Session, "user_id")
        assert col.nullable is False
        fk_targets = [fk.target_fullname for fk in col.foreign_keys]
        assert "users.id" in fk_targets

    def test_session_has_token_hash_column(self) -> None:
        col = _col(Session, "token_hash")
        assert col.nullable is False

    def test_session_has_expires_at_column(self) -> None:
        col = _col(Session, "expires_at")
        assert col.nullable is False

    def test_session_has_is_revoked_column(self) -> None:
        col = _col(Session, "is_revoked")
        assert col.nullable is False

    def test_session_is_revoked_defaults_to_false(self) -> None:
        col = _col(Session, "is_revoked")
        assert col.default.arg is False

    def test_session_has_created_at(self) -> None:
        col = _col(Session, "created_at")
        assert col.nullable is False

    def test_session_has_updated_at(self) -> None:
        col = _col(Session, "updated_at")
        assert col.nullable is False


# ===========================================================================
# User lockout fields tests
# ===========================================================================


class TestUserLockoutFields:
    """Tests for failed_login_count and locked_until on User model."""

    def test_user_has_failed_login_count_column(self) -> None:
        col = _col(User, "failed_login_count")
        assert col is not None

    def test_failed_login_count_is_not_nullable(self) -> None:
        col = _col(User, "failed_login_count")
        assert col.nullable is False

    def test_failed_login_count_defaults_to_zero(self) -> None:
        col = _col(User, "failed_login_count")
        assert col.default.arg == 0

    def test_user_has_locked_until_column(self) -> None:
        col = _col(User, "locked_until")
        assert col is not None

    def test_locked_until_is_nullable(self) -> None:
        col = _col(User, "locked_until")
        assert col.nullable is True
