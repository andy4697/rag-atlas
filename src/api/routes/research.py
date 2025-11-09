"""Research agent endpoints."""

import structlog
from fastapi import APIRouter

from ...models.base import BaseResponse

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=BaseResponse)
async def research_status():
    """Get research agent status."""
    return BaseResponse(
        success=True,
        message="Research agent endpoints - implementation pending",
        data={"status": "not_implemented"},
    )


@router.post("/search", response_model=BaseResponse)
async def search_papers():
    """Search research papers - placeholder endpoint."""
    return BaseResponse(
        success=False,
        message="Search functionality not yet implemented",
        data={"status": "not_implemented"},
    )


@router.post("/ingest", response_model=BaseResponse)
async def ingest_papers():
    """Ingest papers - placeholder endpoint."""
    return BaseResponse(
        success=False,
        message="Ingestion functionality not yet implemented",
        data={"status": "not_implemented"},
    )
