"""ReflectWorkflow module for ReXia.AI's multi-stage reflective task execution system."""

from typing import Any
from ..base import BaseWorkflow, BaseMemory
from ..common import CollaborationChannel, TaskStatus
from ..agents import Component
from ..agents.workers import PlanWorker, FinaliseWorker, Worker, ToolWorker

class ReflectWorkflow(BaseWorkflow):
    """
    ReflectWorkflow class for ReXia.AI, implementing a multi-stage reflective task execution process.

    This class extends BaseWorkflow to provide a specific implementation for tasks that require
    a reflective approach, including planning, tool usage, execution, and finalization stages.
    It orchestrates the interaction between various specialized components to complete complex
    tasks efficiently and thoughtfully.

    Attributes:
        llm (Any): The language model used by the workflow for task processing and decision making.
        task (str): The specific task or objective that the workflow is designed to accomplish.
        verbose (bool): Flag for enabling detailed logging and output for debugging purposes.
        memory (BaseMemory): The memory component used to store and retrieve relevant information across runs.
        channel (CollaborationChannel): Communication channel for task-related interactions and data sharing.
        plan (Component): The component responsible for task planning.
        tool (Component): The component responsible for tool-related operations and interactions.
        work (Component): The component responsible for the main task execution.
        finalise (Component): The component responsible for refining and finalizing the task output.
    """

    llm: Any
    task: str
    verbose: bool
    memory: BaseMemory
    channel: CollaborationChannel
    plan: Component
    tool: Component
    work: Component
    finalise: Component

    def __init__(
        self,
        llm: Any,
        task: str,
        memory: BaseMemory,
        verbose: bool = False,
    ) -> None:
        """
        Initialize a ReflectWorkflow instance.

        Sets up the collaboration channel, memory, and initializes all workflow components
        (plan, tool, work, and finalise).

        Args:
            llm (Any): The language model to be used throughout the workflow.
            task (str): A description of the task to be performed by the workflow.
            memory (BaseMemory): The memory object to be used for storing and retrieving information.
            verbose (bool, optional): Enable verbose mode for detailed logging. Defaults to False.
        """
        super().__init__(llm, task, verbose)
        self.channel = CollaborationChannel(task)
        self.memory = memory
        self.plan = Component(
            "plan",
            self.channel,
            PlanWorker(model=llm, verbose=verbose),
            memory=self.memory,
        )
        self.tool = Component(
            "tool",
            self.channel,
            ToolWorker(model=llm, verbose=verbose),
            memory=self.memory,
        )
        self.work = Component(
            "work",
            self.channel,
            Worker(model=llm, verbose=verbose),
            memory=self.memory,
        )
        self.finalise = Component(
            "finalise",
            self.channel,
            FinaliseWorker(model=llm, verbose=verbose),
            memory=self.memory,
        )

    def _run_task(self) -> None:
        """
        Execute the main task processing logic of the reflective workflow.

        This method orchestrates the execution of the task through multiple stages:
        1. Planning
        2. Tool usage (if available)
        3. Main work execution
        4. Finalization and refinement

        It manages the task status, handles exceptions, and updates the memory with the final result.

        Returns:
            None

        Raises:
            Exception: If an error occurs during task execution. The error is caught and printed.
        """
        try:
            print(f"ReXia.AI is working on the task: {self.channel.task}")

            self.channel.status = TaskStatus.WORKING
            self.plan.run()

            if self.llm.tools:
                self.tool.run()
            self.work.run()

            self.finalise.run()

            self.channel.status = TaskStatus.COMPLETED

            # Add the final message to the memory
            self.memory.add_message(self.channel.messages[-1])

            print(f"ReXia.AI has completed the task: {self.channel.task}")
        except Exception as e:
            print(f"An error occurred while running the task: {e}")

    def run(self) -> None:
        """
        Execute the reflective workflow.

        This method serves as the main entry point for running the reflective workflow.
        It invokes the _run_task method to process the task through all stages.

        Returns:
            None
        """
        self._run_task()