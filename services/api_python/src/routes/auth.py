"""
Authentication routes.
Thin controllers: validate input, call service, return response.
"""

import structlog
from fastapi import APIRouter, Cookie, Depends, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.errors import AppError
from src.middleware.rate_limit import RateLimitConfig, RateLimiter, rate_limit_response
from src.repositories.session_repository import SessionRepository
from src.repositories.user_repository import UserRepository
from src.services.auth_service import AuthService
from src.services.email_service import EmailService
from src.services.token_service import TokenService
from src.types.auth import RegisterRequest, RegisterResponse
from src.types.login import LoginRequest, LoginResponse

log = structlog.get_logger()

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

_rate_limiter = RateLimiter()
_rate_limiter.configure_route(
    "/api/v1/auth/register",
    RateLimitConfig(max_requests=5, window_seconds=900),
)
_rate_limiter.configure_route(
    "/api/v1/auth/login",
    RateLimitConfig(max_requests=10, window_seconds=900),
)
_rate_limiter.configure_route(
    "/api/v1/auth/refresh",
    RateLimitConfig(max_requests=20, window_seconds=900),
)


def _get_auth_service(session: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(
        user_repo=UserRepository(session),
        email_service=EmailService(),
        token_service=TokenService(),
        session_repo=SessionRepository(session),
    )


@router.post("/register", response_model=RegisterResponse, status_code=201)
async def register(
    body: RegisterRequest,
    request: Request,
    service: AuthService = Depends(_get_auth_service),
) -> RegisterResponse | JSONResponse:
    """Register a new user account."""
    log.info("route.register", email=body.email)

    client_ip = request.client.host if request.client else "unknown"
    config = _rate_limiter.get_config("/api/v1/auth/register")
    if config:
        allowed, retry_after = await _rate_limiter.check_rate_limit(
            key=f"register:{client_ip}", config=config
        )
        if not allowed:
            return rate_limit_response(retry_after)

    try:
        user = await service.register(email=body.email, password=body.password, name=body.name)
    except AppError as err:
        return JSONResponse(status_code=err.status_code, content={"detail": err.message})

    return RegisterResponse(id=user.id, email=user.email, name=user.name)


@router.post("/login", response_model=LoginResponse)
async def login(
    body: LoginRequest,
    request: Request,
    response: Response,
    service: AuthService = Depends(_get_auth_service),
) -> LoginResponse | JSONResponse:
    """Authenticate user and return tokens."""
    log.info("route.login", email=body.email)

    client_ip = request.client.host if request.client else "unknown"
    config = _rate_limiter.get_config("/api/v1/auth/login")
    if config:
        allowed, retry_after = await _rate_limiter.check_rate_limit(
            key=f"login:{client_ip}", config=config
        )
        if not allowed:
            return rate_limit_response(retry_after)

    try:
        tokens = await service.login(email=body.email, password=body.password)
    except AppError as err:
        return JSONResponse(status_code=err.status_code, content={"detail": err.message})

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=30 * 24 * 3600,
        path="/api/v1/auth",
    )

    return LoginResponse(
        access_token=tokens["access_token"],
        name=tokens["name"],
        user_id=tokens["user_id"],
    )


@router.post("/logout", status_code=204)
async def logout(
    response: Response,
    refresh_token: str | None = Cookie(None),
    service: AuthService = Depends(_get_auth_service),
) -> Response:
    """Sign out — revoke session server-side and clear cookie."""
    log.info("route.logout")
    if refresh_token:
        await service.logout(refresh_token=refresh_token)

    response.delete_cookie(
        key="refresh_token",
        path="/api/v1/auth",
    )
    response.status_code = 204
    return response
