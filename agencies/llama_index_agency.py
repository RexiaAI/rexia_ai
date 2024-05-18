# llama_index_agency.py
from typing import List, Any
from rexia_ai.agencies import BaseAgency
from rexia_ai.tasks import BaseTask
from rexia_ai.agents import ManagerAgent
from llama_index.core.agent.types import BaseAgent
from llama_index.core.tools.types import BaseTool


class LlamaIndexAgency(BaseAgency):
    """Agency for ReXia AI."""
    def __init__(self, manager: ManagerAgent, agents: List[BaseAgent], tasks: List[BaseTask], tools: List[BaseTool], llm: Any, verbose: bool = True):
        """Initialize the agency."""
        super().__init__(manager, agents, tasks, tools, llm, verbose)