"""SimpleToolWorkflow module for ReXia.AI's streamlined task execution system with tool integration."""

import logging
from typing import Any
from ..base import BaseWorkflow
from ..common import CollaborationChannel, TaskStatus
from ..agents import Component
from ..agents.workers import Worker, ToolWorker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class SimpleToolWorkflow(BaseWorkflow):
    """
    SimpleToolWorkflow class for ReXia.AI, implementing a streamlined task execution process with tool integration.

    This class extends BaseWorkflow to provide a simplified implementation for tasks that may require
    tool usage followed by main task execution. It orchestrates the interaction between a tool component
    and a work component to efficiently complete tasks.

    Attributes:
        llm (Any): The language model used by the workflow for task processing and decision making.
        task (str): The specific task or objective that the workflow is designed to accomplish.
        verbose (bool): Flag for enabling detailed logging and output for debugging purposes.
        channel (CollaborationChannel): Communication channel for task-related interactions and data sharing.
        tool (Component): The component responsible for tool-related operations and interactions.
        work (Component): The component responsible for the main task execution.
    """

    llm: Any
    task: str
    verbose: bool
    channel: CollaborationChannel
    tool: Component
    work: Component

    def __init__(
        self,
        llm: Any,
        task: str,
        verbose: bool = False,
    ) -> None:
        """
        Initialize a SimpleToolWorkflow instance.

        Sets up the collaboration channel, memory, and initializes the tool and work components.

        Args:
            llm (Any): The language model to be used throughout the workflow.
            task (str): A description of the task to be performed by the workflow.
            verbose (bool, optional): Enable verbose mode for detailed logging. Defaults to False.
        """
        super().__init__(llm, task, verbose)
        self.channel = CollaborationChannel(task)
        self.tool = Component(
            "tool",
            self.channel,
            ToolWorker(model=llm, verbose=verbose),
        )
        self.work = Component(
            "work",
            self.channel,
            Worker(model=llm, verbose=verbose),
        )

    def _run_task(self) -> None:
        """
        Execute the main task processing logic of the simple tool workflow.

        This method orchestrates the execution of the task through two main stages:
        1. Tool usage (if tools are available)
        2. Main work execution

        It manages the task status, handles exceptions, and updates the memory with the final result.

        Returns:
            None

        Raises:
            Exception: If an error occurs during task execution. The error is caught and logged.
        """
        try:
            logger.info(f"ReXia.AI is working on the task: {self.channel.task}")

            self.channel.status = TaskStatus.WORKING
            logger.debug(f"Task status set to: {self.channel.status}")

            if self.llm.tools:
                self.tool.run()     
            self.work.run()

            self.channel.status = TaskStatus.COMPLETED
            logger.debug(f"Task status set to: {self.channel.status}")

            # Add the final message to the memory
            final_message = self.channel.messages[-1]
            if self.verbose:
                logger.debug(f"Result: {final_message}")

            logger.info(f"ReXia.AI has completed the task: {self.channel.task}")
        except Exception as e:
            logger.error(f"An error occurred while running the task: {e}", exc_info=True)
            raise

    def run(self) -> None:
        """
        Execute the simple tool workflow.

        This method serves as the main entry point for running the simple tool workflow.
        It invokes the _run_task method to process the task through all stages.

        Returns:
            None
        """
        try:
            self._run_task()
        except Exception as e:
            logger.error(f"Simple tool workflow execution failed: {e}", exc_info=True)