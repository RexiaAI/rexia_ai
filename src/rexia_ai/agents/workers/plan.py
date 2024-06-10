"""planWorker class for ReXia AI."""

from typing import Any, List
from ...base import BaseWorker
from ...thought_buffer import BufferManager


class PlanWorker(BaseWorker):
    """A specialised planning worker for a ReXia.AI agent."""

    model: Any

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
    ):
        super().__init__(model, verbose=verbose)
        self.buffer = BufferManager()

    def create_prompt(self, task: str, messages: List[str]) -> str:
        """Create a prompt for the model."""
        prompt = (
            """
                You are a specialist planning agent.
                You are part of a team working on a task.
                Your job is to think through the task and create a plan to complete it.
                If you are provided with a plan, you should review it and provide a refined version if nessecary, or
                simply supply the plan if it is correct.
            """
            + "\n\n"
            + f"Previous Plan: {self._get_thought_template(task)}"
            + "\n\n"
            + self.get_plan_structured_output_prompt()
            + "\n\n"
            + "Task: "
            + task
            + "\n\n"
            "Collaboration Chat:" + "\n\n".join(messages)
        )
        return prompt
    
    def _get_thought_template(self, task: str) -> str:
        thought_template = self.buffer.get_template(task)
        if thought_template:
            return thought_template
        else:
            return "No thought template found for task."

