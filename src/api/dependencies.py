"""FastAPI dependencies for dependency injection."""

from typing import Annotated

import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..agents.orchestrator import orchestrator
from ..core.config import get_settings

logger = structlog.get_logger(__name__)
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> dict:
    """Get current authenticated user."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
    # For now, return a mock user, implement jwt token
    return {"user_id": "mock_user", "username": "test_user"}


async def get_orchestrator():
    """Get the agent orchestrator instance."""
    return orchestrator


async def get_app_settings():
    """Get application settings."""
    return get_settings()


def require_auth():
    """Dependency that requires authentication."""
    return Depends(get_current_user)


def optional_auth():
    """Dependency for optional authentication."""

    async def _optional_auth(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    ) -> dict | None:
        if not credentials:
            return None
        try:
            return await get_current_user(credentials)
        except HTTPException:
            return None

    return Depends(_optional_auth)
