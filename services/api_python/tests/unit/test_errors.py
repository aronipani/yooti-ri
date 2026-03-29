"""Unit tests for application error hierarchy."""

from src.errors import (
    AppError,
    AuthenticationError,
    AuthorisationError,
    DuplicateEmailError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


class TestAppError:
    """Tests for the base AppError class."""

    def test_message_is_stored(self) -> None:
        err = AppError("something broke")
        assert err.message == "something broke"

    def test_default_status_code_is_500(self) -> None:
        err = AppError("oops")
        assert err.status_code == 500

    def test_custom_status_code(self) -> None:
        err = AppError("bad", status_code=400)
        assert err.status_code == 400

    def test_is_exception(self) -> None:
        err = AppError("x")
        assert isinstance(err, Exception)

    def test_str_representation(self) -> None:
        err = AppError("fail")
        assert str(err) == "fail"


class TestNotFoundError:
    """Tests for NotFoundError."""

    def test_inherits_from_app_error(self) -> None:
        err = NotFoundError("User", "abc-123")
        assert isinstance(err, AppError)

    def test_status_code_is_404(self) -> None:
        err = NotFoundError("User", "abc-123")
        assert err.status_code == 404

    def test_message_contains_resource_and_id(self) -> None:
        err = NotFoundError("User", "abc-123")
        assert err.message == "User not found: abc-123"

    def test_resource_attribute(self) -> None:
        err = NotFoundError("Order", "xyz")
        assert err.resource == "Order"

    def test_resource_id_attribute(self) -> None:
        err = NotFoundError("Order", "xyz")
        assert err.resource_id == "xyz"


class TestDuplicateEmailError:
    """Tests for DuplicateEmailError."""

    def test_inherits_from_app_error(self) -> None:
        err = DuplicateEmailError()
        assert isinstance(err, AppError)

    def test_status_code_is_409(self) -> None:
        err = DuplicateEmailError()
        assert err.status_code == 409

    def test_message(self) -> None:
        err = DuplicateEmailError()
        assert err.message == "An account with this email already exists"


class TestValidationError:
    """Tests for ValidationError."""

    def test_inherits_from_app_error(self) -> None:
        err = ValidationError("bad input")
        assert isinstance(err, AppError)

    def test_status_code_is_422(self) -> None:
        err = ValidationError("bad input")
        assert err.status_code == 422

    def test_message(self) -> None:
        err = ValidationError("email is required")
        assert err.message == "email is required"


class TestRateLimitError:
    """Tests for RateLimitError."""

    def test_inherits_from_app_error(self) -> None:
        err = RateLimitError(retry_after=60)
        assert isinstance(err, AppError)

    def test_status_code_is_429(self) -> None:
        err = RateLimitError(retry_after=60)
        assert err.status_code == 429

    def test_message(self) -> None:
        err = RateLimitError(retry_after=30)
        assert err.message == "Too many requests"

    def test_retry_after_attribute(self) -> None:
        err = RateLimitError(retry_after=120)
        assert err.retry_after == 120


class TestAuthenticationError:
    """Tests for AuthenticationError."""

    def test_inherits_from_app_error(self) -> None:
        err = AuthenticationError()
        assert isinstance(err, AppError)

    def test_status_code_is_401(self) -> None:
        err = AuthenticationError()
        assert err.status_code == 401

    def test_message(self) -> None:
        err = AuthenticationError()
        assert err.message == "Incorrect email or password"


class TestAuthorisationError:
    """Tests for AuthorisationError."""

    def test_inherits_from_app_error(self) -> None:
        err = AuthorisationError()
        assert isinstance(err, AppError)

    def test_status_code_is_403(self) -> None:
        err = AuthorisationError()
        assert err.status_code == 403

    def test_message(self) -> None:
        err = AuthorisationError()
        assert err.message == "Forbidden"
