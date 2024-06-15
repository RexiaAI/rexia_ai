"""Base Workflow for ReXia.AI."""

from typing import Any

class BaseWorkflow:
    """
    BaseWorkflow class for ReXia AI, refactored for better design principles.

    Attributes:
        llm: The language model used by the workflow.
        task: The task that the workflow is designed to perform.
        verbose: A flag used for enabling verbose mode.
    """
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