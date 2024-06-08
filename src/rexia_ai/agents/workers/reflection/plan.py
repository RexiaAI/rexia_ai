"""planWorker class for ReXia AI."""

from typing import Any, List
from ....base import BaseWorker


class PlanWorker(BaseWorker):
    """A specialised planning worker for a ReXia.AI agent."""

    model: Any

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
    ):
        super().__init__(model, verbose=verbose)

    def create_prompt(self, task: str, messages: List[str]) -> str:
        """Create a prompt for the model."""
        prompt = (
            """
                You are a specialist planning agent.
                You are part of a team working on a task.
                Your job is to plan the steps needed to complete the task and provide it to the team.
                Only plan steps that are relevant to the task.
                Make sure to include all the necessary steps to complete the task.
                The result of following the plan should be a completion of the task.
                Your plan should only include steps that can be performed right now.
                Your plan should only include steps an AI can complete.
                Your plan should not include steps that continue after the task is completed, such as review or promotion.
            """
            + "\n\n"
            + self.get_plan_structured_output_prompt()
            + "\n\n"
            + "Task: "
            + task
            + "\n\n"
            "Collaboration Chat:" + "\n\n".join(messages)
        )
        return prompt

