"""WorkAgent class for ReXia AI."""

from typing import List, Optional
from langchain_core.tools import Tool
from ..llms import RexiaAIChatOpenAI
from ..common import WorkflowStateSchema
from ..base import BaseAgent


class WorkAgent(BaseAgent):
    """WorkAgent for ReXia AI."""

    model: RexiaAIChatOpenAI
    tools: Optional[List[Tool]]

    def __init__(
        self, model: RexiaAIChatOpenAI, instructions: str = "", verbose: bool = False
    ):
        super().__init__(model, instructions=instructions, verbose=verbose)

    def action(self, agency_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Work on the current task."""
        graph_state = agency_state

        if self.verbose:
            print(
                f"Worker working on task: {self.get_value_or_default(graph_state, 'task')}"
            )

        prompt = {
            "instructions": (
                self.instructions
                + " Ensure the response adheres to the provided format and guidelines. "
                "Do not give instructions to perform the task. "
                "Your response should be a completion of the task. "
                "Always make changes according to reviewer feedback."
            ),
            "task": self.get_value_or_default(graph_state, "task"),
            "reviewer feedback": self.get_value_or_default(
                graph_state, "feedback"
            ),
            "guidelines": self.get_value_or_default(graph_state, "guidelines"),
            "messages": self.get_value_or_default(graph_state, "messages"),
            "response format": {"message": "Your response here"},
            "example reponse": {"message": "Hello, World!"},
        }

        agent_response = self._invoke_model(prompt, "message")

        if self.verbose:
            print(
                f"Worker response: {self.get_value_or_default(agent_response, 'message')}"
            )

        graph_state["messages"] = self.get_value_or_default(agent_response, "message")
        return graph_state
