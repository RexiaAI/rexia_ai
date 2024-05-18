"""Base Agency Class for ReXia AI."""

from typing import List, Any
from rexia_ai.tasks import BaseTask
from rexia_ai.agents import ManagerAgent
from rexia_ai.agencies.statuses import Status


class BaseAgency:
    """Base Agency Class."""

    def __init__(
        self,
        manager: ManagerAgent,
        agents: List[Any],
        tasks: List[BaseTask],
        tools: List[Any],
        llm: Any,
        verbose: bool = True,
    ):
        """Initialize the agency."""
        self.manager = manager
        self.agents = agents
        self.tasks = tasks
        self.tools = tools
        self.llm = llm
        self.verbose = verbose
        self.status = Status.IDLE

    def launch(self):
        """Launch the agency."""

        self.status = Status.WORKING
