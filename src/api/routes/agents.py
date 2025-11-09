"""Agent management endpoints."""

import structlog
from fastapi import APIRouter, HTTPException

from ...agents.orchestrator import orchestrator
from ...models.base import BaseResponse

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=BaseResponse)
async def list_agents():
    """List all registered agents."""
    try:
        agents = orchestrator.list_agents()
        return BaseResponse(success=True, data={"agents": agents, "count": len(agents)})
    except Exception as e:
        logger.error("Failed to list agents", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to list agents") from e


@router.get("/{agent_name}/info", response_model=BaseResponse)
async def get_agent_info(agent_name: str):
    """Get information about a specific agent."""
    agent = orchestrator.get_agent(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    try:
        info = agent.get_info()
        return BaseResponse(success=True, data=info)
    except Exception as e:
        logger.error("Failed to get agent info", agent_name=agent_name, error=str(e))
        raise HTTPException(
            status_code=500, detail="Failed to get agent information"
        ) from e


@router.get("/{agent_name}/health", response_model=BaseResponse)
async def check_agent_health(agent_name: str):
    """Check health of a specific agent."""
    agent = orchestrator.get_agent(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    try:
        health = await agent.health_check()
        return BaseResponse(success=True, data={"agent": agent_name, "healthy": health})
    except Exception as e:
        logger.error(
            "Failed to check agent health", agent_name=agent_name, error=str(e)
        )
        raise HTTPException(
            status_code=500, detail="Failed to check agent health"
        ) from e


@router.post("/{agent_name}/process", response_model=BaseResponse)
async def process_with_agent(agent_name: str, input_data: dict):
    """Process data with a specific agent."""
    try:
        result = await orchestrator.process_with_agent(agent_name, input_data)

        if result.success:
            return BaseResponse(
                success=True, data=result.data, metadata=result.metadata
            )
        else:
            return BaseResponse(
                success=False,
                message=result.error,
                errors=[result.error] if result.error else None,
            )

    except Exception as e:
        logger.error(
            "Failed to process with agent", agent_name=agent_name, error=str(e)
        )
        raise HTTPException(status_code=500, detail="Failed to process request") from e
