"""Base agent interface and common functionality."""

from abc import ABC, abstractmethod
from typing import Any

import structlog
from pydantic import BaseModel

logger = structlog.get_logger(__name__)


class AgentConfig(BaseModel):
    """Base configuration for agents."""

    name: str
    version: str = "1.0.0"
    enabled: bool = True
    max_retries: int = 3
    timeout_seconds: int = 30


class AgentResult(BaseModel):
    """Base result model for agent operations."""

    success: bool
    data: dict[str, Any] | None = None
    error: str | None = None
    metadata: dict[str, Any] = {}


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = logger.bind(agent=config.name)

    @abstractmethod
    async def process(self, input_data: dict[str, Any]) -> AgentResult:
        """Process input data and return result."""
        pass

    async def health_check(self) -> bool:
        """Check if agent is healthy and ready to process requests."""
        return self.config.enabled

    def get_info(self) -> dict[str, Any]:
        """Get agent information."""
        return {
            "name": self.config.name,
            "version": self.config.version,
            "enabled": self.config.enabled,
        }
