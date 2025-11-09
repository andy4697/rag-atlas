"""FastAPI application factory."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from ..core.config import get_settings
from ..core.logging import get_logger, setup_logging
from .routes import health, research, resume


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    logger = get_logger(__name__)
    logger.info("Starting Multi-Agent RAG System")

    # Startup logic here
    yield

    # Shutdown logic here
    logger.info("Shutting down Multi-Agent RAG System")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    # Setup logging first
    setup_logging()
    logger = get_logger(__name__)

    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Multi-Agent RAG System for Research Papers and Resume Generation",
        lifespan=lifespan,
        debug=settings.debug,
    )

    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.debug else ["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"],
    )

    # Include routers
    app.include_router(
        health.router, prefix=f"{settings.api_prefix}/health", tags=["health"]
    )
    app.include_router(
        research.router, prefix=f"{settings.api_prefix}/research", tags=["research"]
    )
    app.include_router(
        resume.router, prefix=f"{settings.api_prefix}/resume", tags=["resume"]
    )

    # Import agents router
    from .routes import agents

    app.include_router(
        agents.router, prefix=f"{settings.api_prefix}/agents", tags=["agents"]
    )

    logger.info("FastAPI application created", debug=settings.debug)
    return app


# Create app instance
app = create_app()
