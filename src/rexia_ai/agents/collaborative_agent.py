"""Collaborative Agent for ReXia AI."""

from llama_index.core.agent import (
    AgentRunner,
    ReActAgentWorker
)


class CollaborativeAgent(AgentRunner):
    """Collaborative Agent for ReXia AI."""

    def __init__(self, agent_worker: ReActAgentWorker):
        """Initialize the Collaborative Agent."""
        super().__init__(agent_worker=agent_worker)

    def run(self):
        """Run the Collaborative Agent."""
