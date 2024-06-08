"""Worker class for ReXia AI."""

from typing import Any, List
from ....base import BaseWorker


class Worker(BaseWorker):
    """A non-specilaised specialised worker for a ReXia AI agent."""

    model: Any

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
    ):
        super().__init__(model, verbose=verbose)

    def create_prompt(self, task, messages: List[str]) -> str:
        """Create a prompt for the model."""
        prompt = (
            """
                You are a worker agent.
                You are part of a team working on a task.
                Read the collaboration chat and the task fully to understand the context and plan.
                Your job is to complete the task.
                Do not add any explanation or reasoning to your answer outside your chain of reasoning.
            """
            + "\n\n"
            + self.get_structured_output_prompt()
            + "\n\n"
            + "Task: "
            + task
            + "\n\n"
            "Collaboration Chat:" + "\n\n".join(messages)
        )
        return prompt

