"""Agent orchestrator for managing multiple agents."""

import structlog

from .base import AgentResult, BaseAgent

logger = structlog.get_logger(__name__)


class AgentOrchestrator:
    """Orchestrates multiple agents and manages their lifecycle."""

    def __init__(self):
        self._agents: dict[str, BaseAgent] = {}
        self.logger = logger.bind(component="orchestrator")

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the orchestrator."""
        self._agents[agent.config.name] = agent
        self.logger.info("Agent registered", agent_name=agent.config.name)

    def get_agent(self, name: str) -> BaseAgent | None:
        """Get an agent by name."""
        return self._agents.get(name)

    def list_agents(self) -> list[str]:
        """List all registered agent names."""
        return list(self._agents.keys())

    async def health_check_all(self) -> dict[str, bool]:
        """Check health of all registered agents."""
        results = {}
        for name, agent in self._agents.items():
            try:
                results[name] = await agent.health_check()
            except Exception as e:
                self.logger.error("Health check failed", agent_name=name, error=str(e))
                results[name] = False
        return results

    async def process_with_agent(
        self, agent_name: str, input_data: dict
    ) -> AgentResult:
        """Process data with a specific agent."""
        agent = self.get_agent(agent_name)
        if not agent:
            return AgentResult(success=False, error=f"Agent '{agent_name}' not found")

        try:
            return await agent.process(input_data)
        except Exception as e:
            self.logger.error(
                "Agent processing failed", agent_name=agent_name, error=str(e)
            )
            return AgentResult(success=False, error=f"Processing failed: {str(e)}")


# Global orchestrator instance
orchestrator = AgentOrchestrator()
