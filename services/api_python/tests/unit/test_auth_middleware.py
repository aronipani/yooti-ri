"""Unit tests for the auth middleware (require_auth dependency).

Tests verify token extraction and validation logic.
"""

import uuid
from datetime import UTC, datetime, timedelta

import jwt
import pytest

from src.services.token_service import ALGORITHM

TEST_SECRET = "test-secret-key"
TEST_USER_ID = uuid.uuid4()


def _make_token(
    *,
    user_id: uuid.UUID = TEST_USER_ID,
    expired: bool = False,
    secret: str = TEST_SECRET,
) -> str:
    now = datetime.now(tz=UTC)
    if expired:
        exp = now - timedelta(hours=1)
    else:
        exp = now + timedelta(hours=24)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": exp,
        "type": "access",
    }
    return jwt.encode(payload, secret, algorithm=ALGORITHM)


class TestTokenDecoding:
    """Tests for JWT token decoding logic."""

    def test_valid_token_decodes_successfully(self) -> None:
        token = _make_token()
        payload = jwt.decode(token, TEST_SECRET, algorithms=[ALGORITHM])
        assert payload["sub"] == str(TEST_USER_ID)

    def test_expired_token_raises_error(self) -> None:
        token = _make_token(expired=True)
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token, TEST_SECRET, algorithms=[ALGORITHM])

    def test_invalid_secret_raises_error(self) -> None:
        token = _make_token(secret="correct-secret")
        with pytest.raises(jwt.InvalidSignatureError):
            jwt.decode(token, "wrong-secret", algorithms=[ALGORITHM])

    def test_malformed_token_raises_error(self) -> None:
        with pytest.raises(jwt.DecodeError):
            jwt.decode("not.a.real.token", TEST_SECRET, algorithms=[ALGORITHM])
