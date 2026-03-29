"""
Session repository — database queries for session management.
"""

import hashlib
import uuid
from datetime import UTC, datetime

import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession as DBSession

from src.models.session import Session

log = structlog.get_logger()


class SessionRepository:
    """Data access layer for sessions."""

    def __init__(self, session: DBSession) -> None:
        self._session = session

    async def create_session(
        self,
        *,
        user_id: uuid.UUID,
        token: str,
        expires_at: datetime,
    ) -> Session:
        """Create a new session record."""
        log.info("repository.create_session", user_id=str(user_id))
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        session_obj = Session(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self._session.add(session_obj)
        await self._session.flush()
        return session_obj

    async def revoke_session(self, *, token: str) -> None:
        """Revoke a session by its token."""
        log.info("repository.revoke_session")
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        await self._session.execute(
            update(Session).where(Session.token_hash == token_hash).values(is_revoked=True)
        )

    async def is_session_valid(self, *, token: str) -> bool:
        """Check if a session exists, is not revoked, and has not expired."""
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        result = await self._session.execute(
            select(Session).where(
                Session.token_hash == token_hash,
                Session.is_revoked.is_(False),
                Session.expires_at > datetime.now(tz=UTC),
            )
        )
        return result.scalars().first() is not None

    async def revoke_all_for_user(self, *, user_id: uuid.UUID) -> None:
        """Revoke all sessions for a user."""
        log.info("repository.revoke_all_for_user", user_id=str(user_id))
        await self._session.execute(
            update(Session).where(Session.user_id == user_id).values(is_revoked=True)
        )
