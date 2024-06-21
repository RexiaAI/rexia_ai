"""Base Workflow for ReXia.AI."""

from typing import Any
from abc import ABC, abstractmethod


class BaseWorkflow(ABC):
    """
    BaseWorkflow class for ReXia AI, allows for the creation of workflows from a standard interface.

    Attributes:
        llm: The language model used by the workflow.
        task: The task that the workflow is designed to perform.
        verbose: A flag used for enabling verbose mode.
    """

    llm: Any
    task: str
    verbose: bool

    def __init__(self, llm: Any, task: str, verbose: bool = False):
        """
        Initialize a BaseWorkflow instance.

        Args:
            llm: The language model used by the workflow.
            task: The task that the workflow is designed to perform.
            verbose: A flag used for enabling verbose mode. Defaults to False.
        """
        self.llm = llm
        self.task = task
        self.verbose = verbose

    @abstractmethod
    def run(self) -> str:
        pass
