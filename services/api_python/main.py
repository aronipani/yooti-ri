"""
yooti-ri — FastAPI application entry point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from src.config import settings
from src.middleware.logging import LoggingMiddleware
from src.routes.health import router as health_router
from src.routes.auth import router as auth_router
from src.routes.cart import router as cart_router
from src.routes.products import router as products_router

log = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("api.startup", environment=settings.environment)
    yield
    log.info("api.shutdown")


app = FastAPI(
    title="yooti-ri API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

app.include_router(health_router)
app.include_router(products_router)
app.include_router(auth_router)
app.include_router(cart_router)
