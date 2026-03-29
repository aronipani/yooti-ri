"""Unit tests for AuthService.

All external dependencies (repositories, email) are mocked.
"""

import uuid
from unittest.mock import AsyncMock, MagicMock

import bcrypt
import pytest

from src.errors import DuplicateEmailError
from src.services.auth_service import BCRYPT_COST, AuthService


def _build_service(
    *,
    existing_user: MagicMock | None = None,
) -> tuple[AuthService, AsyncMock, AsyncMock]:
    user_repo = AsyncMock()
    user_repo.get_by_email.return_value = existing_user

    created_user = MagicMock()
    created_user.id = uuid.uuid4()
    created_user.email = "new@example.com"
    created_user.name = "New User"
    user_repo.create_user.return_value = created_user

    email_service = AsyncMock()

    service = AuthService(user_repo=user_repo, email_service=email_service)
    return service, user_repo, email_service


class TestRegister:
    """Tests for AuthService.register."""

    @pytest.mark.anyio
    async def test_creates_user_with_hashed_password(self) -> None:
        service, user_repo, _ = _build_service()

        await service.register(email="test@example.com", password="securepass", name="Test")

        user_repo.create_user.assert_called_once()
        call_kwargs = user_repo.create_user.call_args.kwargs
        assert call_kwargs["email"] == "test@example.com"
        assert call_kwargs["name"] == "Test"
        assert bcrypt.checkpw(
            b"securepass",
            call_kwargs["password_hash"].encode("utf-8"),
        )

    @pytest.mark.anyio
    async def test_password_hashed_with_bcrypt_cost_12(self) -> None:
        service, user_repo, _ = _build_service()

        await service.register(email="test@example.com", password="securepass", name="Test")

        call_kwargs = user_repo.create_user.call_args.kwargs
        hash_bytes = call_kwargs["password_hash"].encode("utf-8")
        rounds = int(hash_bytes.split(b"$")[2])
        assert rounds == BCRYPT_COST

    @pytest.mark.anyio
    async def test_raises_duplicate_email_error_for_existing_user(self) -> None:
        existing = MagicMock()
        existing.email = "taken@example.com"
        service, _, _ = _build_service(existing_user=existing)

        with pytest.raises(DuplicateEmailError):
            await service.register(email="taken@example.com", password="securepass", name="Test")

    @pytest.mark.anyio
    async def test_sends_welcome_email_on_success(self) -> None:
        service, _, email_service = _build_service()

        await service.register(email="new@example.com", password="securepass", name="New User")

        email_service.send_welcome_email.assert_called_once_with(
            email="new@example.com", name="New User"
        )

    @pytest.mark.anyio
    async def test_does_not_send_email_on_duplicate(self) -> None:
        existing = MagicMock()
        service, _, email_service = _build_service(existing_user=existing)

        with pytest.raises(DuplicateEmailError):
            await service.register(email="taken@example.com", password="pw12345678", name="Test")

        email_service.send_welcome_email.assert_not_called()

    @pytest.mark.anyio
    async def test_returns_created_user(self) -> None:
        service, _, _ = _build_service()

        result = await service.register(
            email="new@example.com", password="securepass", name="New User"
        )

        assert result.email == "new@example.com"
        assert result.name == "New User"


class TestVerifyPassword:
    """Tests for AuthService.verify_password."""

    def test_correct_password_returns_true(self) -> None:
        hashed = bcrypt.hashpw(b"mypassword", bcrypt.gensalt(rounds=4)).decode("utf-8")
        assert AuthService.verify_password("mypassword", hashed) is True

    def test_wrong_password_returns_false(self) -> None:
        hashed = bcrypt.hashpw(b"mypassword", bcrypt.gensalt(rounds=4)).decode("utf-8")
        assert AuthService.verify_password("wrongpassword", hashed) is False
