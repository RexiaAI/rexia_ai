# base_agency.py
from typing import List, Any
from tasks import BaseTask
from rexia_ai.agents import ManagerAgent

class BaseAgency:
    """Base Agency Class for ReXia AI."""
    def __init__(self, manager: ManagerAgent, agents: List[Any], tasks: List[BaseTask], tools: List[Any], llm: Any, verbose: bool = True):
        """Initialize the agency."""
        self.agents = agents
        self.tasks = tasks
        self.tools = tools
        self.llm = llm
        self.verbose = verbose
    
    def launch(self):
        """Launch the agency."""
        pass