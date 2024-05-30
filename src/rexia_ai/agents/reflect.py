"""ReflectWorker class for ReXia AI."""

from typing import List, Optional
from langchain_core.tools import Tool
from ..llms import ReXiaAIChatOpenAI
from ..base import BaseWorker


class ReflectWorker(BaseWorker):
    """A specialised reflection worker for a ReXia.AI agent."""

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
                You are a specialist reflection agent.
                You are part of a team working on a task.
                Your job is to read the collaboration chat and reflect on how to improve the answer to the task.
                Based on your reflection, you should provide a revised answer to the task that
                improves on the original answer.
            """
            + "\n\n"
            + "Task: "
            + task
            + "\n\n"
            "Collaboration Chat:" + "\n\n".join(messages)
        )
        return prompt

