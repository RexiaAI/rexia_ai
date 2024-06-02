"""ToolWorker class for ReXia AI."""

from typing import List, Optional
from langchain_core.tools import Tool
from ....llms import ReXiaAIChatOpenAI
from ....base import BaseWorker


class ToolWorker(BaseWorker):
    """A specialised tool calling worker for a ReXia AI agent."""

    model: ReXiaAIChatOpenAI
    tools: Optional[List[Tool]]

    def __init__(
        self,
        model: ReXiaAIChatOpenAI,
        verbose: bool = False,
    ):
        super().__init__(model, verbose=verbose)

    def create_prompt(self, task: str, messages: List[str]) -> str:
        """Create a prompt for the model."""
        prompt = (
            """
                You are a tool calling agent.
                You are part of a team working on a task.
                Your job is to gather information for the task using your tools and provide it to the team.
                Only gather information that is relevant to the task.
            """
            + "\n\n"
            + "Task: "
            + task
            + "\n\n"
            "Collaboration Chat:" + "\n\n".join(messages)
        )
        return prompt

