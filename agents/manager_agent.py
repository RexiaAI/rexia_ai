"""Manager Agent for ReXia AI."""

from llama_index.core.agent import AgentRunner
from rexia_ai.agents.manager_agent_worker import ManagerAgentWorker


class ManagerAgent(AgentRunner):
    """Manager Agent for ReXia AI."""

    def __init__(self, agent_worker: ManagerAgentWorker):
        """Initialize the Manager Agent."""
        super().__init__(agent_worker=agent_worker)

    def run(self):
        """Run the Manager Agent."""
