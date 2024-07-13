"""CodeToolWorkflow module for ReXia.AI's Code Tool Generation and Execution system."""

from typing import Any
from ..base import BaseWorkflow, BaseMemory
from ..common import CollaborationChannel, TaskStatus
from ..agents import Component
from ..agents.workers import LLMTool, Worker

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
        max_attempts (int): Maximum number of attempts for code generation before giving up.
        code_tool (Component): The component responsible for generating and executing the code tool.
    """

    def __init__(
        self,
        llm: Any,
        task: str,
        memory: BaseMemory,
        verbose: bool = False,
        max_attempts: int = 5,
    ):
        """
        Initialize a CodeToolWorkflow instance.

        Sets up the collaboration channel, memory, and initializes the LLMTool component.

        Args:
            llm (Any): The language model to be used throughout the workflow.
            task (str): A description of the task to be performed using the code tool.
            memory (BaseMemory): The memory object to be used for storing and retrieving information.
            verbose (bool, optional): Enable verbose mode for detailed logging. Defaults to False.
            max_attempts (int, optional): Maximum number of attempts for code generation. Defaults to 5.
        """
        super().__init__(llm, task, verbose)
        self.memory = memory
        self.channel = CollaborationChannel(task)
        self.max_attempts = max_attempts
        self.code_tool = Component(
            "Code",
            self.channel,
            LLMTool(model=llm, verbose=verbose, max_attempts=max_attempts),
            memory=self.memory,
        )
        self.worker = Component(
            "Work",
            self.channel,
            Worker(model=llm, verbose=verbose, max_attempts=max_attempts),
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
            print(f"ReXia.AI is working on the Code Tool task: {self.task}")

            self.channel.status = TaskStatus.WORKING
            
            # Generate and execute the code tool
            self.code_tool.run()
            self.worker.run()

            self.channel.status = TaskStatus.COMPLETED

            # Add the final message to the memory
            self.memory.add_message(self.channel.messages[-1])

            print(f"ReXia.AI has completed the Code Tool task: {self.channel.task}")

        except Exception as e:
            print(f"An error occurred while running the task: {e}")

    def run(self) -> str:
        """
        Execute the Code Tool workflow.

        This method serves as the main entry point for running the Code Tool workflow.
        It invokes the _run_task method to process the task through all stages.

        Returns:
            str: A success message or an error message if an exception occurs.
        """
        return self._run_task()