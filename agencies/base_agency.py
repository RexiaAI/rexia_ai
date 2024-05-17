# base_agency.py
from typing import List, Any
from tasks import BaseTask

class BaseAgency:
    """Agency for ReXia AI."""
    def __init__(self, agents: List[Any], tasks: List[BaseTask], tools: List[Any], llm: Any, verbose: bool = True):
        """Initialize the agency."""
        self.agents = agents
        self.tasks = tasks
        self.tools = tools
        self.llm = llm
        self.verbose = verbose