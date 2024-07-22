"""CodeToolWorkflow module for ReXia.AI's Code Tool Generation and Execution system."""

import logging
from typing import Any
from ..base import BaseWorkflow, BaseMemory
from ..common import CollaborationChannel, TaskStatus
from ..agents import Component
from ..agents.workers import CodeTool, CodeWorker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class CodeToolWorkflow(BaseWorkflow):
    """
    CodeToolWorkflow class for ReXia.AI, implementing a workflow for generating and executing code tools.

    This class extends BaseWorkflow to provide a specialized implementation for tasks that involve
    generating code tools using a language model and executing them in a containerized environment.

    Attributes:
        llm (Any): The language model used by the workflow for code generation and processing.
        task (str): The specific task or objective that the workflow is designed to accomplish.
        verbose (bool): Flag for enabling detailed logging and output for debugging purposes.
        memory (BaseMemory): The memory component used to store and retrieve relevant information across runs.
        channel (CollaborationChannel): Communication channel for task-related interactions and data sharing.
        code_tool (Component): The component responsible for generating and executing the code tool.
    """

    def __init__(
        self,
        llm: Any,
        task: str,
        memory: BaseMemory,
        verbose: bool = False,
    ):
        """
        Initialize a CodeToolWorkflow instance.

        Sets up the collaboration channel, memory, and initializes the LLMTool component.

        Args:
            llm (Any): The language model to be used throughout the workflow.
            task (str): A description of the task to be performed using the code tool.
            memory (BaseMemory): The memory object to be used for storing and retrieving information.
            verbose (bool, optional): Enable verbose mode for detailed logging. Defaults to False.
        """
        super().__init__(llm, task, verbose)
        self.memory = memory
        self.channel = CollaborationChannel(task)
        self.code_tool = Component(
            "Code",
            self.channel,
            CodeTool(model=llm, verbose=verbose),
            memory=self.memory,
        )
        self.worker = Component(
            "Work",
            self.channel,
            CodeWorker(model=llm, verbose=verbose),
            memory=self.memory
        )

    def _run_task(self) -> None:
        """
        Execute the main Code Tool workflow logic.

        This method orchestrates the process of generating and executing a code tool,
        including setting up the LLMTool worker, generating the code, and executing it.
        It manages the task status, handles exceptions, and updates the memory with the final result.

        Returns:
            str: A success message or an error message if an exception occurs.
        """
        try:
            logger.info(f"ReXia.AI is working on the Code Tool task: {self.task}")

            self.channel.status = TaskStatus.WORKING
            logger.debug(f"Task status set to: {self.channel.status}")
            
            # Generate and execute the code tool
            self.code_tool.run()
            self.worker.run()

            self.channel.status = TaskStatus.COMPLETED
            logger.debug(f"Task status set to: {self.channel.status}")

            # Add the final message to the memory
            final_message = self.channel.messages[-1]
            self.memory.add_message(final_message)
            logger.info("Result added to memory")
            if self.verbose:
                logger.debug(f"Result: {final_message}")

            logger.info(f"ReXia.AI has completed the Code Tool task: {self.channel.task}")

        except Exception as e:
            logger.error(f"An error occurred while running the task: {e}", exc_info=True)
            raise

    def run(self) -> str:
        """
        Execute the Code Tool workflow.

        This method serves as the main entry point for running the Code Tool workflow.
        It invokes the _run_task method to process the task through all stages.

        Returns:
            str: A success message or an error message if an exception occurs.
        """
        try:
            result = self._run_task()
            return result
        except Exception as e:
            logger.error(f"Code Tool workflow execution failed: {e}", exc_info=True)
            return f"An error occurred: {str(e)}"