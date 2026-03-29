"""Unit tests for login/logout/lockout in AuthService.

All external dependencies (repositories, email, tokens) are mocked.
"""

import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import bcrypt
import pytest

from src.errors import AuthenticationError
from src.services.auth_service import MAX_FAILED_LOGINS, AuthService


def _make_user(
    *,
    password: str = "correct-password",
    failed_login_count: int = 0,
    locked_until: datetime | None = None,
) -> MagicMock:
    user = MagicMock()
    user.id = uuid.uuid4()
    user.email = "user@example.com"
    user.name = "Test User"
    user.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=4)).decode(
        "utf-8"
    )
    user.failed_login_count = failed_login_count
    user.locked_until = locked_until
    user.is_active = True
    return user


def _build_service(
    *,
    user: MagicMock | None = None,
) -> tuple[AuthService, AsyncMock, AsyncMock, MagicMock]:
    user_repo = AsyncMock()
    user_repo.get_by_email.return_value = user

    email_service = AsyncMock()

    token_service = MagicMock()
    token_service.create_access_token.return_value = "access-token-123"
    token_service.create_refresh_token.return_value = "refresh-token-456"

    session_repo = AsyncMock()

    service = AuthService(
        user_repo=user_repo,
        email_service=email_service,
        token_service=token_service,
        session_repo=session_repo,
    )
    return service, user_repo, session_repo, token_service


class TestLogin:
    """Tests for AuthService.login."""

    @pytest.mark.anyio
    async def test_valid_credentials_return_tokens(self) -> None:
        user = _make_user()
        service, _, _, _ = _build_service(user=user)

        result = await service.login(email="user@example.com", password="correct-password")

        assert result["access_token"] == "access-token-123"
        assert result["refresh_token"] == "refresh-token-456"
        assert result["name"] == "Test User"

    @pytest.mark.anyio
    async def test_creates_session_on_success(self) -> None:
        user = _make_user()
        service, _, session_repo, _ = _build_service(user=user)

        await service.login(email="user@example.com", password="correct-password")

        session_repo.create_session.assert_called_once()

    @pytest.mark.anyio
    async def test_wrong_password_raises_authentication_error(self) -> None:
        user = _make_user(password="correct-password")
        service, _, _, _ = _build_service(user=user)

        with pytest.raises(AuthenticationError):
            await service.login(email="user@example.com", password="wrong-password")

    @pytest.mark.anyio
    async def test_nonexistent_user_raises_authentication_error(self) -> None:
        service, _, _, _ = _build_service(user=None)

        with pytest.raises(AuthenticationError):
            await service.login(email="nobody@example.com", password="anything")

    @pytest.mark.anyio
    async def test_generic_error_message_on_bad_credentials(self) -> None:
        service, _, _, _ = _build_service(user=None)

        with pytest.raises(AuthenticationError) as exc_info:
            await service.login(email="nobody@example.com", password="anything")

        assert exc_info.value.message == "Incorrect email or password"

    @pytest.mark.anyio
    async def test_locked_account_raises_authentication_error(self) -> None:
        locked = datetime.now(tz=UTC) + timedelta(minutes=30)
        user = _make_user(locked_until=locked)
        service, _, _, _ = _build_service(user=user)

        with pytest.raises(AuthenticationError):
            await service.login(email="user@example.com", password="correct-password")

    @pytest.mark.anyio
    async def test_ten_failures_lock_account(self) -> None:
        user = _make_user(failed_login_count=MAX_FAILED_LOGINS - 1)
        service, _, _, _ = _build_service(user=user)

        with pytest.raises(AuthenticationError):
            await service.login(email="user@example.com", password="wrong")

        assert user.locked_until is not None
        assert user.locked_until > datetime.now(tz=UTC)

    @pytest.mark.anyio
    async def test_successful_login_resets_failed_count(self) -> None:
        user = _make_user(failed_login_count=3)
        service, _, _, _ = _build_service(user=user)

        await service.login(email="user@example.com", password="correct-password")

        assert user.failed_login_count == 0
        assert user.locked_until is None


class TestLogout:
    """Tests for AuthService.logout."""

    @pytest.mark.anyio
    async def test_logout_revokes_session(self) -> None:
        service, _, session_repo, _ = _build_service()

        await service.logout(refresh_token="some-token")

        session_repo.revoke_session.assert_called_once_with(token="some-token")
