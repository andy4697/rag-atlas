"""Resume agent endpoints."""

import structlog
from fastapi import APIRouter

from ...models.base import BaseResponse

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=BaseResponse)
async def resume_status():
    """Get resume agent status."""
    return BaseResponse(
        success=True,
        message="Resume agent endpoints - implementation pending",
        data={"status": "not_implemented"},
    )


@router.post("/upload", response_model=BaseResponse)
async def upload_resume():
    """Upload resume - placeholder endpoint."""
    return BaseResponse(
        success=False,
        message="Resume upload functionality not yet implemented",
        data={"status": "not_implemented"},
    )


@router.post("/analyze", response_model=BaseResponse)
async def analyze_resume():
    """Analyze resume - placeholder endpoint."""
    return BaseResponse(
        success=False,
        message="Resume analysis functionality not yet implemented",
        data={"status": "not_implemented"},
    )
