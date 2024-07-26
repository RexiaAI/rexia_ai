"""CodeWorkflow module for ReXia.AI's Code Generation."""

import logging
from typing import Any
from ..base import BaseWorkflow
from ..common import CollaborationChannel, TaskStatus
from ..agents import Component
from ..agents.workers import CodeWorker, ToolWorker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class CodeWorkflow(BaseWorkflow):
    """
    CodeWorkflow class for ReXia.AI, implementing a workflow for generating code.

    This class extends BaseWorkflow to provide a specialized implementation for tasks that involve
    generating code using a language model.

    Attributes:
        llm (Any): The language model used by the workflow for code generation and processing.
        task (str): The specific task or objective that the workflow is designed to accomplish.
        verbose (bool): Flag for enabling detailed logging and output for debugging purposes.
        channel (CollaborationChannel): Communication channel for task-related interactions and data sharing.
        code (Component): The component responsible for generating the code.
    """

    def __init__(
        self,
        llm: Any,
        task: str,
        verbose: bool = False,
    ):
        """
        Initialize a CodeWorkflow instance.

        Sets up the collaboration channel, memory, and initializes the Code component.

        Args:
            llm (Any): The language model to be used throughout the workflow.
            task (str): A description of the task to be performed using the code tool.
            verbose (bool, optional): Enable verbose mode for detailed logging. Defaults to False.
        """
        super().__init__(llm, task, verbose)
        self.channel = CollaborationChannel(task)
        self.tool = Component(
            "Tool",
            self.channel,
            ToolWorker(model=llm, verbose=verbose),
        )
        self.code = Component(
            "Code",
            self.channel,
            CodeWorker(model=llm, verbose=verbose),
        )

    def _run_task(self) -> None:
        """
        Execute the main Code workflow logic.

        This method orchestrates the process of generating code,
        including setting up the Code worker and generating the code.
        It manages the task status, handles exceptions, and updates the memory with the final result.

        Returns:
            str: A success message or an error message if an exception occurs.
        """
        try:
            logger.info(f"ReXia.AI is working on the Code task: {self.task}")

            self.channel.status = TaskStatus.WORKING
            logger.debug(f"Task status set to: {self.channel.status}")
            
            if self.llm.tools:
                self.tool.run()
            
            self.code.run()

            self.channel.status = TaskStatus.COMPLETED
            logger.debug(f"Task status set to: {self.channel.status}")

            # Add the final message to the memory
            final_message = self.channel.messages[-1]
            if self.verbose:
                logger.debug(f"Result: {final_message}")

            logger.info(f"ReXia.AI has completed the Code Tool task: {self.channel.task}")

        except Exception as e:
            logger.error(f"An error occurred while running the task: {e}", exc_info=True)
            raise

    def run(self) -> str:
        """
        Execute the Code workflow.

        This method serves as the main entry point for running the Code workflow.
        It invokes the _run_task method to process the task through all stages.

        Returns:
            str: A success message or an error message if an exception occurs.
        """
        try:
            result = self._run_task()
            return result
        except Exception as e:
            logger.error(f"Code workflow execution failed: {e}", exc_info=True)
            return f"An error occurred: {str(e)}"