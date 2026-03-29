"""
Token service — JWT encode/decode for authentication.
"""

import uuid
from datetime import UTC, datetime, timedelta

import jwt
import structlog

from src.config import settings

log = structlog.get_logger()

ACCESS_TOKEN_EXPIRE_HOURS = 24
REFRESH_TOKEN_EXPIRE_DAYS = 30
ALGORITHM = "HS256"


class TokenService:
    """Handles JWT token creation and verification."""

    def __init__(self, secret_key: str | None = None) -> None:
        self._secret_key = secret_key or settings.jwt_secret_key

    def create_access_token(self, *, user_id: uuid.UUID) -> str:
        """Create a signed JWT access token."""
        now = datetime.now(tz=UTC)
        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),
            "type": "access",
        }
        return jwt.encode(payload, self._secret_key, algorithm=ALGORITHM)

    def create_refresh_token(self, *, user_id: uuid.UUID) -> str:
        """Create a signed JWT refresh token."""
        now = datetime.now(tz=UTC)
        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            "type": "refresh",
        }
        return jwt.encode(payload, self._secret_key, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> dict[str, str]:
        """Decode and verify a JWT token. Raises jwt.PyJWTError on failure."""
        payload: dict[str, str] = jwt.decode(token, self._secret_key, algorithms=[ALGORITHM])
        return payload
