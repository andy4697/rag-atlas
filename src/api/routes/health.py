"""Health check endpoints."""

import time
from datetime import datetime

import structlog
from fastapi import APIRouter, Depends

from ...agents.orchestrator import orchestrator
from ...core.config import get_settings
from ...models.base import HealthCheckResponse

logger = structlog.get_logger(__name__)
router = APIRouter()

# Track application start time
start_time = time.time()


@router.get("/", response_model=HealthCheckResponse)
async def health_check(settings=Depends(get_settings)):
    """Basic health check endpoint."""
    uptime = time.time() - start_time

    # Check agent health
    agent_health = await orchestrator.health_check_all()

    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        components=agent_health,
        uptime_seconds=uptime,
    )


@router.get("/ready")
async def readiness_check():
    """Readiness check for Kubernetes."""
    # Check if all critical components are ready
    agent_health = await orchestrator.health_check_all()

    if all(agent_health.values()) or len(agent_health) == 0:
        return {"status": "ready"}
    else:
        return {"status": "not ready", "components": agent_health}


@router.get("/live")
async def liveness_check():
    """Liveness check for Kubernetes."""
    return {"status": "alive", "timestamp": datetime.utcnow()}
