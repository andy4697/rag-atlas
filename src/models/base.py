"""Base data models and common types."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class TimestampMixin(BaseModel):
    """Mixin for models that need timestamp fields."""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None


class StatusEnum(str, Enum):
    """Common status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BaseResponse(BaseModel):
    """Base response model for API endpoints."""

    success: bool
    message: str | None = None
    data: Any | None = None
    errors: list[str] | None = None
    metadata: dict[str, Any] = {}


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints."""

    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        """Calculate offset from page and size."""
        return (self.page - 1) * self.size


class PaginatedResponse(BaseModel):
    """Paginated response model."""

    items: list[Any]
    total: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(cls, items: list[Any], total: int, pagination: PaginationParams):
        """Create paginated response."""
        pages = (total + pagination.size - 1) // pagination.size
        return cls(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
            pages=pages,
        )


class HealthCheckResponse(BaseModel):
    """Health check response model."""

    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str
    components: dict[str, bool] = {}
    uptime_seconds: float | None = None
