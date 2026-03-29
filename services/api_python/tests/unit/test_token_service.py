"""Unit tests for TokenService.

Tests JWT creation and decoding without hitting external services.
"""

import uuid

import jwt
import pytest

from src.services.token_service import ALGORITHM, TokenService

SECRET = "test-secret-key-at-least-32-chars!"
USER_ID = uuid.uuid4()


def _service() -> TokenService:
    return TokenService(secret_key=SECRET)


class TestCreateAccessToken:
    """Tests for TokenService.create_access_token."""

    def test_returns_string(self) -> None:
        token = _service().create_access_token(user_id=USER_ID)
        assert isinstance(token, str)

    def test_contains_user_id_in_sub(self) -> None:
        token = _service().create_access_token(user_id=USER_ID)
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        assert payload["sub"] == str(USER_ID)

    def test_contains_access_type(self) -> None:
        token = _service().create_access_token(user_id=USER_ID)
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        assert payload["type"] == "access"

    def test_has_exp_claim(self) -> None:
        token = _service().create_access_token(user_id=USER_ID)
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        assert "exp" in payload


class TestCreateRefreshToken:
    """Tests for TokenService.create_refresh_token."""

    def test_returns_string(self) -> None:
        token = _service().create_refresh_token(user_id=USER_ID)
        assert isinstance(token, str)

    def test_contains_refresh_type(self) -> None:
        token = _service().create_refresh_token(user_id=USER_ID)
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        assert payload["type"] == "refresh"

    def test_contains_user_id_in_sub(self) -> None:
        token = _service().create_refresh_token(user_id=USER_ID)
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        assert payload["sub"] == str(USER_ID)


class TestDecodeToken:
    """Tests for TokenService.decode_token."""

    def test_decodes_valid_access_token(self) -> None:
        svc = _service()
        token = svc.create_access_token(user_id=USER_ID)
        payload = svc.decode_token(token)
        assert payload["sub"] == str(USER_ID)

    def test_raises_on_invalid_token(self) -> None:
        svc = _service()
        with pytest.raises(jwt.PyJWTError):
            svc.decode_token("garbage.token.here")

    def test_raises_on_wrong_secret(self) -> None:
        token = TokenService(secret_key="secret-A-at-least-32-characters!!").create_access_token(
            user_id=USER_ID
        )
        with pytest.raises(jwt.InvalidSignatureError):
            TokenService(secret_key="secret-B-at-least-32-characters!!").decode_token(token)
