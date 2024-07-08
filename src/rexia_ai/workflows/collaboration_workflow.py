"""CollaborationWorkflow module for ReXia.AI's multi-agent task execution system."""

from typing import Any
from ..base import BaseWorkflow, BaseMemory
from ..common import CollaborationChannel, TaskStatus
from ..agents import Component
from ..agents.workers import TeamWorker, ToolWorker

class CollaborationWorkflow(BaseWorkflow):
    """
    CollaborationWorkflow class for ReXia.AI, implementing a multi-agent collaborative task execution process.

    This class extends BaseWorkflow to provide a specific implementation for tasks that require
    collaboration between different components, particularly team work and tool usage. It orchestrates
    the interaction between various agents to complete complex tasks efficiently.

    Attributes:
        llm (Any): The language model used by the workflow for task processing and decision making.
        task (str): The specific task or objective that the workflow is designed to accomplish.
        verbose (bool): Flag for enabling detailed logging and output for debugging purposes.
        memory (BaseMemory): The memory component used to store and retrieve relevant information across runs.
        channel (CollaborationChannel): Communication channel for task-related interactions and data sharing.
        team_work (Component): The component responsible for team-based collaborative work.
        tool (Component): The component responsible for tool-related operations and interactions.
    """

    llm: Any
    task: str
    verbose: bool
    memory: BaseMemory
    channel: CollaborationChannel
    team_work: Component
    tool: Component

    def __init__(
        self,
        llm: Any,
        task: str,
        memory: BaseMemory,
        verbose: bool = False,
        max_attempts: int = 3,
    ) -> None:
        """
        Initialize a CollaborationWorkflow instance.

        Sets up the collaboration channel, memory, and initializes the team work and tool components.

        Args:
            llm (Any): The language model to be used throughout the workflow.
            task (str): A description of the task to be performed by the workflow.
            memory (BaseMemory): The memory object to be used for storing and retrieving information.
            verbose (bool, optional): Enable verbose mode for detailed logging. Defaults to False.
            max_attempts (int, optional): Maximum number of attempts for each component. Defaults to 3.
        """
        super().__init__(llm, task, verbose)
        self.channel = CollaborationChannel(task)
        self.memory = memory
        self.team_work = Component(
            "team work",
            self.channel,
            TeamWorker(model=llm, verbose=verbose, max_attempts=max_attempts),
            memory=self.memory,
        )
        self.tool = Component(
            "tool",
            self.channel,
            ToolWorker(model=llm, verbose=verbose, max_attempts=max_attempts),
            memory=self.memory,
        )

    def _run_task(self) -> None:
        """
        Execute the main task processing logic of the workflow.

        This method orchestrates the execution of the task, including tool usage (if available)
        and team work. It manages the task status, handles exceptions, and updates the memory
        with the final result.

        Returns:
            None

        Raises:
            Exception: If an error occurs during task execution. The error is caught and printed.
        """
        try:
            print(f"ReXia.AI is working on the task: {self.channel.task}")

            self.channel.status = TaskStatus.WORKING
            if self.llm.tools:
                self.tool.run()
            self.team_work.run()

            self.channel.status = TaskStatus.COMPLETED

            # Add the final message to the memory
            self.memory.add_message(self.channel.messages[-1])

            print(f"ReXia.AI has completed the task: {self.channel.task}")
        except Exception as e:
            print(f"An error occurred while running the task: {e}")

    def run(self) -> None:
        """
        Execute the collaboration workflow.

        This method serves as the main entry point for running the collaboration workflow.
        It invokes the _run_task method to process the task.

        Returns:
            None
        """
        self._run_task()