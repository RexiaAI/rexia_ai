"""TDDWorkflow module for ReXia.AI's Test-Driven Development task execution system."""

import logging
from typing import Any
from ..base import BaseWorkflow
from ..common import CollaborationChannel, TaskStatus
from ..agents import Component
from ..agents.workers import TDDWorker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class TDDWorkflow(BaseWorkflow):
    """
    TDDWorkflow class for ReXia.AI, implementing a Test-Driven Development approach using a language model.

    This class extends BaseWorkflow to provide a specialized implementation for tasks that follow
    Test-Driven Development (TDD) principles. It orchestrates the interaction between a TDD worker
    component and the language model to generate code that passes predefined tests.

    Attributes:
        llm (Any): The language model used by the workflow for code generation and processing.
        task (str): The specific task or objective that the workflow is designed to accomplish.
        verbose (bool): Flag for enabling detailed logging and output for debugging purposes.
        channel (CollaborationChannel): Communication channel for task-related interactions and data sharing.
        max_attempts (int): Maximum number of attempts for code generation before giving up.
        tdd (Component): The component responsible for executing the TDD process.
        test_class (type): The class containing the test cases to be used in the TDD process.
    """

    def __init__(
        self,
        llm: Any,
        task: str,
        verbose: bool = False,
    ):
        """
        Initialize a TDDWorkflow instance.

        Sets up the collaboration channel, memory, and initializes the TDD component.

        Args:
            llm (Any): The language model to be used throughout the workflow.
            task (str): A description of the task to be performed using TDD.
            verbose (bool, optional): Enable verbose mode for detailed logging. Defaults to False.
        """
        super().__init__(llm, task, verbose)
        self.channel = CollaborationChannel(task)
        self.test_class = None
        self.tdd = Component(
            "tdd",
            self.channel,
            TDDWorker(model=llm, verbose=verbose),
        )

    def _run_task(self) -> None:
        """
        Execute the main TDD workflow logic.

        This method orchestrates the TDD process, including setting up the TDD worker,
        running the tests, and generating code. It manages the task status, handles exceptions,
        and updates the memory with the final result.

        Returns:
            str: A success message or an error message if an exception occurs.

        Raises:
            ValueError: If the test class has not been set before running the workflow.
        """
        try:
            logger.info(f"ReXia.AI is working on the TDD task: {self.task}")

            self.channel.status = TaskStatus.WORKING
            logger.debug(f"Task status set to: {self.channel.status}")
            
            if self.test_class is None:
                logger.error("Test class has not been set.")
                raise ValueError("Test class has not been set. Use set_test_class() before running the workflow.")
            
            # Set up the TDD worker
            self.tdd.worker.set_test_class(self.test_class)
            self.tdd.run()

            self.channel.status = TaskStatus.COMPLETED
            logger.debug(f"Task status set to: {self.channel.status}")

            # Add the final message to the memory
            final_message = self.channel.messages[-1]
            if self.verbose:
                logger.debug(f"Result: {final_message}")

            logger.info(f"ReXia.AI has completed the TDD task: {self.channel.task}")

        except Exception as e:
            logger.error(f"An error occurred while running the task: {e}", exc_info=True)
            raise

    def set_test_class(self, test_class: type) -> None:
        """
        Set the test class to be used in the TDD process.

        This method sets the test class for both the workflow and the TDD worker.

        Args:
            test_class (type): The class containing the test cases for the TDD process.

        Returns:
            None
        """
        self.test_class = test_class
        # Set the test class on the worker as well
        self.tdd.worker.set_test_class(test_class)
        logger.info(f"Test class set: {test_class.__name__}")
        
    def run(self) -> str:
        """
        Execute the TDD workflow.

        This method serves as the main entry point for running the TDD workflow.
        It invokes the _run_task method to process the task through all stages.

        Returns:
            str: A success message or an error message if an exception occurs.
        """
        try:
            result = self._run_task()
            return result
        except Exception as e:
            logger.error(f"TDD workflow execution failed: {e}", exc_info=True)
            return f"An error occurred: {str(e)}"