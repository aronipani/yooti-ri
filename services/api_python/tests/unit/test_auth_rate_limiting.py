"""Unit tests for auth endpoint rate limiting.

Tests verify rate limiter logic — no Redis required for unit tests.
"""

from unittest.mock import AsyncMock

import pytest

from src.middleware.rate_limit import RateLimitConfig, RateLimiter, rate_limit_response


class TestRateLimiter:
    """Tests for the RateLimiter class."""

    @pytest.mark.anyio
    async def test_allows_requests_under_limit(self) -> None:
        redis = AsyncMock()
        redis.incr.return_value = 1
        redis.expire.return_value = True

        limiter = RateLimiter(redis_client=redis)
        config = RateLimitConfig(max_requests=10, window_seconds=900)

        allowed, retry_after = await limiter.check_rate_limit(key="login:1.2.3.4", config=config)

        assert allowed is True
        assert retry_after == 0

    @pytest.mark.anyio
    async def test_blocks_after_exceeding_limit(self) -> None:
        redis = AsyncMock()
        redis.incr.return_value = 11
        redis.ttl.return_value = 600

        limiter = RateLimiter(redis_client=redis)
        config = RateLimitConfig(max_requests=10, window_seconds=900)

        allowed, retry_after = await limiter.check_rate_limit(key="login:1.2.3.4", config=config)

        assert allowed is False
        assert retry_after == 600

    @pytest.mark.anyio
    async def test_first_request_sets_expire(self) -> None:
        redis = AsyncMock()
        redis.incr.return_value = 1
        redis.expire.return_value = True

        limiter = RateLimiter(redis_client=redis)
        config = RateLimitConfig(max_requests=5, window_seconds=3600)

        await limiter.check_rate_limit(key="register:1.2.3.4", config=config)

        redis.expire.assert_called_once_with("ratelimit:register:1.2.3.4", 3600)

    @pytest.mark.anyio
    async def test_graceful_degradation_on_redis_failure(self) -> None:
        redis = AsyncMock()
        redis.incr.side_effect = ConnectionError("Redis down")

        limiter = RateLimiter(redis_client=redis)
        config = RateLimitConfig(max_requests=10, window_seconds=900)

        allowed, retry_after = await limiter.check_rate_limit(key="login:1.2.3.4", config=config)

        assert allowed is True
        assert retry_after == 0

    @pytest.mark.anyio
    async def test_allows_all_when_no_redis(self) -> None:
        limiter = RateLimiter(redis_client=None)
        config = RateLimitConfig(max_requests=1, window_seconds=60)

        allowed, _ = await limiter.check_rate_limit(key="test", config=config)

        assert allowed is True

    @pytest.mark.anyio
    async def test_login_blocks_after_10_requests_in_15_minutes(self) -> None:
        redis = AsyncMock()
        redis.incr.return_value = 11
        redis.ttl.return_value = 850

        limiter = RateLimiter(redis_client=redis)
        config = RateLimitConfig(max_requests=10, window_seconds=900)

        allowed, retry_after = await limiter.check_rate_limit(key="login:5.6.7.8", config=config)

        assert allowed is False
        assert retry_after > 0

    @pytest.mark.anyio
    async def test_register_blocks_after_5_requests_in_1_hour(self) -> None:
        redis = AsyncMock()
        redis.incr.return_value = 6
        redis.ttl.return_value = 3200

        limiter = RateLimiter(redis_client=redis)
        config = RateLimitConfig(max_requests=5, window_seconds=3600)

        allowed, retry_after = await limiter.check_rate_limit(key="register:5.6.7.8", config=config)

        assert allowed is False
        assert retry_after > 0

    @pytest.mark.anyio
    async def test_refresh_blocks_after_20_requests_in_15_minutes(self) -> None:
        redis = AsyncMock()
        redis.incr.return_value = 21
        redis.ttl.return_value = 700

        limiter = RateLimiter(redis_client=redis)
        config = RateLimitConfig(max_requests=20, window_seconds=900)

        allowed, retry_after = await limiter.check_rate_limit(key="refresh:5.6.7.8", config=config)

        assert allowed is False
        assert retry_after > 0


class TestRateLimitResponse:
    """Tests for the 429 response builder."""

    def test_returns_429_status(self) -> None:
        resp = rate_limit_response(60)
        assert resp.status_code == 429

    def test_includes_retry_after_header(self) -> None:
        resp = rate_limit_response(120)
        assert resp.headers.get("retry-after") == "120"

    def test_includes_error_detail(self) -> None:
        resp = rate_limit_response(60)
        assert b"Too many requests" in resp.body


class TestRateLimitConfig:
    """Tests for per-route configuration."""

    def test_configure_and_retrieve_route(self) -> None:
        limiter = RateLimiter()
        config = RateLimitConfig(max_requests=10, window_seconds=900)
        limiter.configure_route("/api/v1/auth/login", config)

        result = limiter.get_config("/api/v1/auth/login")
        assert result is not None
        assert result.max_requests == 10
        assert result.window_seconds == 900

    def test_returns_none_for_unconfigured_route(self) -> None:
        limiter = RateLimiter()
        assert limiter.get_config("/api/v1/unknown") is None
