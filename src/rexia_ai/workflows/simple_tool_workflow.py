"""SimpleToolWorkflow class for ReXia.AI"""

from typing import Any
from ..base import BaseWorkflow, BaseMemory
from ..common import CollaborationChannel, TaskStatus
from ..agents import Component
from ..agents.workers import Worker, ToolWorker

class SimpleToolWorkflow(BaseWorkflow):
    """
    SimpleToolWorkflow Class for ReXia AI, refactored for better design principles.

    Attributes:
        llm: The language model used by the workflow.
        task: The task that the workflow is designed to perform.
        verbose: A flag used for enabling verbose mode.
        memory: The memory component of the workflow.
        channel: The collaboration channel for the workflow.
        tool: The tool component of the workflow.
        work: The work component of the workflow.
    """

    llm: Any
    task: str
    verbose: bool
    memory: BaseMemory
    channel: CollaborationChannel
    tool: Component
    work: Component

    def __init__(
        self,
        llm: Any,
        task: str,
        memory: BaseMemory,
        verbose: bool = False,
        max_attempts: int = 3,
    ) -> None:
        super().__init__(llm, task, verbose)
        self.channel = CollaborationChannel(task)
        self.memory = memory
        self.tool = Component(
            "tool",
            self.channel,
            ToolWorker(model=llm, verbose=verbose, max_attempts=max_attempts),
            memory=self.memory,
        )
        self.work = Component(
            "work",
            self.channel,
            Worker(model=llm, verbose=verbose, max_attempts=max_attempts),
            memory=self.memory,
        )

    def _run_task(self):
        """Run the agent process."""
        try:
            print(f"ReXia.AI is working on the task: {self.channel.task}")

            self.channel.status = TaskStatus.WORKING

            if self.llm.tools:
                self.tool.run()
            self.work.run()

            self.channel.status = TaskStatus.COMPLETED

            # Add the final message to the memory
            self.memory.add_message(self.channel.messages[-1])

            print(f"ReXia.AI has completed the task: {self.channel.task}")
        except Exception as e:
            print(f"An error occurred while running the task: {e}")

    def run(self):
        """Run the agent."""
        self._run_task()