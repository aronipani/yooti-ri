"""
Auth service — business logic for registration and authentication.
"""

import asyncio
import time
from datetime import UTC, datetime, timedelta

import bcrypt
import structlog

from src.errors import AuthenticationError, DuplicateEmailError
from src.models.user import User
from src.repositories.session_repository import SessionRepository
from src.repositories.user_repository import UserRepository
from src.services.email_service import EmailService
from src.services.token_service import TokenService

log = structlog.get_logger()

BCRYPT_COST = 12
CONSTANT_TIME_SECONDS = 0.3
MAX_FAILED_LOGINS = 10
LOCKOUT_DURATION_MINUTES = 30


class AuthService:
    """Business logic for authentication flows."""

    def __init__(
        self,
        user_repo: UserRepository,
        email_service: EmailService,
        token_service: TokenService | None = None,
        session_repo: SessionRepository | None = None,
    ) -> None:
        self._user_repo = user_repo
        self._email_service = email_service
        self._token_service = token_service
        self._session_repo = session_repo

    async def register(
        self,
        *,
        email: str,
        password: str,
        name: str,
    ) -> User:
        """Register a new user account.

        Raises DuplicateEmailError if the email is already taken.
        Uses constant-time comparison to prevent email enumeration.
        """
        log.info("service.register", email=email)
        start = time.monotonic()

        existing = await self._user_repo.get_by_email(email)
        if existing:
            elapsed = time.monotonic() - start
            remaining = max(0, CONSTANT_TIME_SECONDS - elapsed)
            await asyncio.sleep(remaining)
            raise DuplicateEmailError()

        password_hash = self._hash_password(password)

        user = await self._user_repo.create_user(
            email=email,
            password_hash=password_hash,
            name=name,
        )

        await self._email_service.send_welcome_email(email=email, name=name)

        elapsed = time.monotonic() - start
        remaining = max(0, CONSTANT_TIME_SECONDS - elapsed)
        await asyncio.sleep(remaining)

        log.info("service.register.complete", user_id=str(user.id))
        return user

    async def login(
        self,
        *,
        email: str,
        password: str,
    ) -> dict[str, str]:
        """Authenticate user and return tokens.

        Raises AuthenticationError on bad credentials or locked account.
        Returns dict with access_token, refresh_token, and user name.
        """
        assert self._token_service is not None
        assert self._session_repo is not None

        log.info("service.login", email=email)
        user = await self._user_repo.get_by_email(email)

        if not user:
            raise AuthenticationError()

        if self._is_locked(user):
            raise AuthenticationError()

        if not self.verify_password(password, user.password_hash):
            await self._increment_failed_login(user)
            raise AuthenticationError()

        await self._reset_failed_login(user)

        access_token = self._token_service.create_access_token(user_id=user.id)
        refresh_token = self._token_service.create_refresh_token(user_id=user.id)

        expires_at = datetime.now(tz=UTC) + timedelta(hours=24)
        await self._session_repo.create_session(
            user_id=user.id, token=refresh_token, expires_at=expires_at
        )

        log.info("service.login.complete", user_id=str(user.id))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "name": user.name,
            "user_id": str(user.id),
        }

    async def logout(self, *, refresh_token: str) -> None:
        """Revoke the session associated with the refresh token."""
        assert self._session_repo is not None
        log.info("service.logout")
        await self._session_repo.revoke_session(token=refresh_token)

    @staticmethod
    def _is_locked(user: User) -> bool:
        """Check if the user account is currently locked."""
        if user.locked_until is None:
            return False
        return user.locked_until > datetime.now(tz=UTC)

    async def _increment_failed_login(self, user: User) -> None:
        """Increment failed login counter and lock if threshold reached."""
        new_count = user.failed_login_count + 1
        user.failed_login_count = new_count
        if new_count >= MAX_FAILED_LOGINS:
            user.locked_until = datetime.now(tz=UTC) + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            log.warning("service.account_locked", user_id=str(user.id))

    @staticmethod
    async def _reset_failed_login(user: User) -> None:
        """Reset failed login counter after successful auth."""
        user.failed_login_count = 0
        user.locked_until = None

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password with bcrypt at the configured cost factor."""
        salt = bcrypt.gensalt(rounds=BCRYPT_COST)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against a bcrypt hash."""
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
