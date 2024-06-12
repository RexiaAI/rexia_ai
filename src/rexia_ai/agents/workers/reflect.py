"""reflectWorker class for ReXia AI."""

from typing import Any, List
from ...base import BaseWorker


class ReflectWorker(BaseWorker):
    """A specialised reflection worker for a ReXia.AI agent."""

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
                You are a specialist reflection agent.
                You are part of a team working on a task.
                Your job is to read the collaboration chat and reflect on how to improve the answer to the task.
                Based on your reflection, you should provide a revised answer to the task that
                improves on the original answer.
                Don't use abreveations or shorthand in your reflection if they are not explained in the answer.
                Don't give instructions on how to improve the answer, just provide the improved answer.
                If there is a message from tools in the collaboration chat, use the output from the tools in your work.
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

