"""
Application error hierarchy.
All domain errors extend AppError.
Never throw raw Exception() — always use a specific error subclass.
"""


class AppError(Exception):
    """Base class for all application errors."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, resource_id: str) -> None:
        super().__init__(f"{resource} not found: {resource_id}", status_code=404)
        self.resource = resource
        self.resource_id = resource_id


class DuplicateEmailError(AppError):
    """Raised when attempting to register with an already-used email."""

    def __init__(self) -> None:
        super().__init__("An account with this email already exists", status_code=409)


class ValidationError(AppError):
    """Raised when input data fails validation."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=422)


class RateLimitError(AppError):
    """Raised when a client exceeds the request rate limit."""

    def __init__(self, retry_after: int) -> None:
        super().__init__("Too many requests", status_code=429)
        self.retry_after = retry_after


class AuthenticationError(AppError):
    """Raised when credentials are invalid."""

    def __init__(self) -> None:
        super().__init__("Incorrect email or password", status_code=401)


class AuthorisationError(AppError):
    """Raised when an authenticated user lacks permission."""

    def __init__(self) -> None:
        super().__init__("Forbidden", status_code=403)
