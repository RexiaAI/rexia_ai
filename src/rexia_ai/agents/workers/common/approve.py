"""ApprovalWorker class for ReXia.AI."""

from typing import Any, List
from ....base import BaseWorker


class ApproveWorker(BaseWorker):
    """A worker agent for deciding if a task has been completed."""

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
                You are an approval agent.
                You are part of a team working on a task.
                Your job is to read the collaboration chat and decide if the task has been completed
                and give feedback.
                Your feedback should consist of a chain of thought explaining your decision followed be
                either "COMPLETED" or "NOT COMPLETED" depending on your decision.
                If the task has been completed, you should approve it by saying "COMPLETED".
                If the task has not been completed, you should say "NOT COMPLETED".
                Only use "COMPLETED" or "NOT COMPLETED" when deciding approval.
            """
            + "\n\n"
            + "Task: "
            + task
            + "\n\n"
            "Collaboration Chat:" + "\n\n".join(messages)
        )
        return prompt

