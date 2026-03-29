"""
User repository — database queries for user accounts.
"""

import uuid

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User

log = structlog.get_logger()


class UserRepository:
    """Data access layer for users."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> User | None:
        """Return a user by email, or None if not found."""
        log.info("repository.get_by_email", email=email)
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_by_email_or_id(
        self,
        *,
        user_id: uuid.UUID | None = None,
        email: str | None = None,
    ) -> User | None:
        """Return a user by ID or email."""
        if user_id:
            result = await self._session.execute(select(User).where(User.id == user_id))
            return result.scalars().first()
        if email:
            return await self.get_by_email(email)
        return None

    async def create_user(
        self,
        *,
        email: str,
        password_hash: str,
        name: str,
    ) -> User:
        """Create and persist a new user."""
        log.info("repository.create_user", email=email)
        user = User(
            email=email,
            password_hash=password_hash,
            name=name,
        )
        self._session.add(user)
        await self._session.flush()
        return user
