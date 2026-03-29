"""
Email service — interface for sending emails.
This is an interface only; actual implementation will use a provider like SendGrid.
"""

import structlog

log = structlog.get_logger()


class EmailService:
    """Email dispatch interface."""

    async def send_welcome_email(self, *, email: str, name: str) -> None:
        """Send a welcome email to a newly registered user."""
        log.info("email.send_welcome", email=email, name=name)
