"""Worker class for ReXia AI."""

from typing import List, Optional
from langchain_core.tools import Tool
from ..llms import ReXiaAIChatOpenAI
from ..base import BaseWorker


class Worker(BaseWorker):
    """A non-specilaised specialised worker for a ReXia AI agent."""

    model: ReXiaAIChatOpenAI
    tools: Optional[List[Tool]]

    def __init__(
        self,
        model: ReXiaAIChatOpenAI,
        verbose: bool = False,
    ):
        super().__init__(model, verbose=verbose)

    def create_prompt(self, task, messages: List[str]) -> str:
        """Create a prompt for the model."""
        prompt = (
            """
                You are a worker agent.
                You are part of a team working on a task.
                Read the collaboration chat and the task fully to understand the context.
                Your job is to follow the plan in the collaboration chat and complete the task.
                Make sure to follow the plan and complete the task.
                Do not deviate from the plan.
                Your result should be the completion of the task.
                Do not do anything that is not part of the plan.
            """
            + "\n\n"
            + "Task: "
            + task
            + "\n\n"
            "Collaboration Chat:" + "\n\n".join(messages)
        )
        return prompt

