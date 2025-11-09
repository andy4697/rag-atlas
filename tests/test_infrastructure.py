"""Test basic infrastructure components."""

import pytest

from src.agents.base import AgentConfig, AgentResult, BaseAgent
from src.agents.orchestrator import orchestrator
from src.core.config import get_settings
from src.models.base import BaseResponse, HealthCheckResponse
from src.utils.helpers import generate_hash, generate_id


def test_settings_loading():
    """Test that settings can be loaded."""
    settings = get_settings()
    assert settings.app_name == "Multi-Agent RAG System"
    assert settings.app_version == "0.1.0"


def test_agent_config():
    """Test agent configuration."""
    config = AgentConfig(name="test_agent")
    assert config.name == "test_agent"
    assert config.version == "1.0.0"
    assert config.enabled is True


class MockAgent(BaseAgent):
    """Mock agent for testing."""

    async def process(self, input_data):
        return AgentResult(success=True, data={"processed": True})


def test_agent_orchestrator():
    """Test agent orchestrator."""
    config = AgentConfig(name="mock_agent")
    agent = MockAgent(config)
    orchestrator.register_agent(agent)
    assert "mock_agent" in orchestrator.list_agents()
    retrieved_agent = orchestrator.get_agent("mock_agent")
    assert retrieved_agent is not None
    assert retrieved_agent.config.name == "mock_agent"


@pytest.mark.asyncio
async def test_agent_processing():
    """Test agent processing."""
    config = AgentConfig(name="test_agent")
    agent = MockAgent(config)
    result = await agent.process({"test": "data"})
    assert result.success is True
    assert result.data["processed"] is True


def test_base_response():
    """Test base response model."""
    response = BaseResponse(success=True, message="Test message")
    assert response.success is True
    assert response.message == "Test message"


def test_health_check_response():
    """Test health check response model."""
    response = HealthCheckResponse(
        status="healthy", version="1.0.0", components={"agent1": True}
    )
    assert response.status == "healthy"
    assert response.version == "1.0.0"
    assert response.components["agent1"] is True


def test_utility_functions():
    """Test utility functions."""
    # Test ID generation
    id1 = generate_id()
    id2 = generate_id()
    assert id1 != id2
    assert len(id1) == 36  # UUID format
    # Test hash generation
    hash1 = generate_hash("test content")
    hash2 = generate_hash("test content")
    hash3 = generate_hash("different content")
    assert len(hash1) == 64  # SHA-256 hex length
    assert hash1 == hash2
    assert hash1 != hash3
