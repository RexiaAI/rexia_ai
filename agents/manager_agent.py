# manager_agent.py

from rexia_ai.agents import AgentRunnner, ManagerAgentWorker

class ManagerAgent(AgentRunnner):
    """Manager Agent for ReXia AI."""
    def __init__(self, agent_worker: ManagerAgentWorker):
        """Initialize the Manager Agent."""
        super().__init__(agent_worker=agent_worker)

    def run(self):
        """Run the Manager Agent."""
        pass