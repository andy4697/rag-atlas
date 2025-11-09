"""Base service classes and interfaces."""

from abc import ABC, abstractmethod
from typing import Any

import structlog
from pydantic import BaseModel

logger = structlog.get_logger(__name__)


class ServiceConfig(BaseModel):
    """Base configuration for services."""

    name: str
    enabled: bool = True
    max_connections: int = 10
    timeout_seconds: int = 30


class ServiceResult(BaseModel):
    """Base result model for service operations."""

    success: bool
    data: Any | None = None
    error: str | None = None
    metadata: dict[str, Any] = {}


class BaseService(ABC):
    """Abstract base class for all services."""

    def __init__(self, config: ServiceConfig):
        self.config = config
        self.logger = logger.bind(service=config.name)
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the service."""
        if self._initialized:
            return

        await self._initialize()
        self._initialized = True
        self.logger.info("Service initialized")

    @abstractmethod
    async def _initialize(self) -> None:
        """Service-specific initialization logic."""
        pass

    async def shutdown(self) -> None:
        """Shutdown the service."""
        if not self._initialized:
            return

        await self._shutdown()
        self._initialized = False
        self.logger.info("Service shutdown")

    @abstractmethod
    async def _shutdown(self) -> None:
        """Service-specific shutdown logic."""
        pass

    async def health_check(self) -> bool:
        """Check if service is healthy."""
        return self._initialized and self.config.enabled

    def get_info(self) -> dict[str, Any]:
        """Get service information."""
        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "initialized": self._initialized,
        }
