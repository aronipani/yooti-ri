"""
Redis-backed rate limiter middleware.
Supports per-route configuration and graceful degradation when Redis is unavailable.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from redis.asyncio import Redis
from starlette.responses import JSONResponse

log = structlog.get_logger()


class RateLimitConfig:
    """Configuration for a rate-limited route."""

    def __init__(self, *, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds


class RateLimiter:
    """Redis-backed sliding window rate limiter."""

    def __init__(self, redis_client: Redis | None = None) -> None:
        self._redis = redis_client
        self._route_configs: dict[str, RateLimitConfig] = {}

    def configure_route(self, path: str, config: RateLimitConfig) -> None:
        """Register rate limit config for a route."""
        self._route_configs[path] = config

    def get_config(self, path: str) -> RateLimitConfig | None:
        """Get rate limit config for a route, if any."""
        return self._route_configs.get(path)

    async def check_rate_limit(self, *, key: str, config: RateLimitConfig) -> tuple[bool, int]:
        """Check if a request is within rate limits.

        Returns (allowed, retry_after_seconds).
        """
        if self._redis is None:
            return True, 0

        try:
            redis_key = f"ratelimit:{key}"
            current = await self._redis.incr(redis_key)

            if current == 1:
                await self._redis.expire(redis_key, config.window_seconds)

            if current > config.max_requests:
                ttl = await self._redis.ttl(redis_key)
                retry_after = max(ttl, 1)
                return False, retry_after

            return True, 0
        except Exception as exc:
            log.warning("rate_limit.redis_unavailable", error=str(exc))
            return True, 0


def rate_limit_response(retry_after: int) -> JSONResponse:
    """Build a 429 Too Many Requests response with Retry-After header."""
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please try again later."},
        headers={"Retry-After": str(retry_after)},
    )
