"""Base Workflow module for ReXia.AI's task execution and management system."""

from typing import Any
from abc import ABC, abstractmethod
from ..common import CollaborationChannel

class BaseWorkflow(ABC):
    """
    Abstract base class for creating standardized workflows in ReXia.AI.

    This class provides a foundation for implementing various task execution workflows
    within the ReXia.AI system. It defines the basic structure and common functionality
    that all specific workflow implementations should follow.

    Attributes:
        llm (Any): The language model used by the workflow for task processing and decision making.
        task (str): The specific task or objective that the workflow is designed to accomplish.
        verbose (bool): Flag for enabling detailed logging and output for debugging purposes.
        channel (CollaborationChannel): Communication channel for task-related interactions and data sharing.

    The BaseWorkflow class is designed to be subclassed, with concrete implementations
    providing specific logic for the `run` method.
    """

    llm: Any
    task: str
    verbose: bool
    channel: CollaborationChannel

    def __init__(self, llm: Any, task: str, verbose: bool = False):
        """
        Initialize a BaseWorkflow instance.

        Sets up the core components needed for workflow execution, including
        the language model, task definition, verbosity setting, and a dedicated
        collaboration channel.

        Args:
            llm (Any): The language model to be used throughout the workflow.
            task (str): A description of the task to be performed by the workflow.
            verbose (bool, optional): Enable verbose mode for detailed logging. Defaults to False.
        """
        self.llm = llm
        self.task = task
        self.verbose = verbose
        self.channel = CollaborationChannel(task)
        
    def clear_channel(self) -> None:
        """
        Clear all messages from the collaboration channel.

        This method resets the communication history in the channel,
        which can be useful when starting a new phase of the task or
        when preparing for a new run of the workflow.

        Returns:
            None
        """
        self.channel.clear_messages()

    @abstractmethod
    def run(self) -> str:
        """
        Execute the workflow to complete the specified task.

        This abstract method must be implemented by all subclasses to define
        the specific steps and logic of the workflow. The implementation should
        utilize the language model, task information, and collaboration channel
        to process the task and produce a result.

        Returns:
            str: The result or output of the workflow execution.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        pass