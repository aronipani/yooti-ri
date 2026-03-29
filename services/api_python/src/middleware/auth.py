"""
Authentication middleware — FastAPI dependency for protected routes.
Extracts JWT from Authorization header and injects current user.
"""

import uuid

import jwt
import structlog
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import get_db
from src.errors import AuthenticationError
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.services.token_service import ALGORITHM

log = structlog.get_logger()

_bearer_scheme = HTTPBearer(auto_error=False)


async def require_auth(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    session: AsyncSession = Depends(get_db),
) -> User:
    """FastAPI dependency that extracts and verifies the JWT, then returns the User.

    Raises AuthenticationError if token is missing, expired, or invalid.
    """
    if credentials is None:
        raise AuthenticationError()

    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        log.warning("auth.token_expired")
        raise AuthenticationError() from None
    except jwt.PyJWTError:
        log.warning("auth.invalid_token")
        raise AuthenticationError() from None

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise AuthenticationError()

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise AuthenticationError() from None

    user_repo = UserRepository(session)
    user = await user_repo.get_by_email_or_id(user_id=user_id)
    if user is None or not user.is_active:
        raise AuthenticationError()

    return user
