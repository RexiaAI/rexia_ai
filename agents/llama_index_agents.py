# llama_index_agents.py
from llama_index.core.agent import AgentRunner, StructuredPlannerAgent, ReActAgent 
from llama_index.core.agent.types import BaseAgentWorker

class AgentRunnner(AgentRunner):
    """This class is a wrapper for llama_index.core.agent.AgentRunner"""
    def __init__(self, agent_worker: BaseAgentWorker):
        """Initialize the Llama Index Agent Runner."""
        super().__init__(agent_worker=agent_worker)

class StructuredPlannerAgent(StructuredPlannerAgent):
    """This class is a wrapper for llama_index.core.agent.StructuredPlannerAgent"""
    def __init__(self, agent_worker: BaseAgentWorker):
        """Initialize the Llama Index Structured Planner Agent."""
        super().__init__(agent_worker=agent_worker)
        
class ReActAgent(ReActAgent):
    """This class is a wrapper for llama_index.core.agent.ReActAgent"""
    def __init__(self, agent_worker: BaseAgentWorker):
        """Initialize the Llama Index ReAct Agent."""
        super().__init__(agent_worker=agent_worker)