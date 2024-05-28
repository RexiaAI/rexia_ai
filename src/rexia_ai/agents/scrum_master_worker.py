"""ScrumMasterWorker class for ReXia AI."""

from typing import List, Optional
from langchain_core.tools import Tool
from ..llms import ReXiaAIChatOpenAI
from ..base import BaseWorker


class ScrumMasterWorker(BaseWorker):
    """ScrumMasterWorker for ReXia AI."""

    model: ReXiaAIChatOpenAI
    tools: Optional[List[Tool]]

    def __init__(
        self,
        model: ReXiaAIChatOpenAI,
        verbose: bool = False,
    ):
        super().__init__(model, verbose=verbose)

    def action(self, task: str, messages: List[str]) -> str:
        """Work on the current task."""

        prompt = self._create_prompt(task, messages)

        agent_response = self._invoke_model(prompt)

        if self.verbose:
            print(f"Scrum Master messsage: {agent_response}")

        return "Scrum Master: " + agent_response

    def _create_prompt(self, task: str, messages: List[str]) -> str:
        """Create a prompt for the model."""
        prompt = ("Task: "
            + task
            + "\n\n"
            "Collaboration Chat:" + "\n\n".join(messages)
        )
        return prompt