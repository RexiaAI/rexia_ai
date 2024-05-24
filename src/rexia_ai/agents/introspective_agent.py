"""IntrospectriveAgent class for ReXia AI."""

from typing import List, Optional
from langchain_core.tools import Tool
from ..llms import RexiaAIChatOpenAI
from ..common import WorkflowStateSchema
from ..base import BaseAgent


class IntrospectiveAgent(BaseAgent):
    """IntrospectiveAgent for ReXia AI."""

    model: RexiaAIChatOpenAI
    tools: Optional[List[Tool]]

    def __init__(
        self, model: RexiaAIChatOpenAI, instructions: str = "", verbose: bool = False
    ):
        super().__init__(model, instructions=instructions, verbose=verbose)

    def action(self, agency_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Perform introspection on the current task."""
        graph_state = agency_state

        if self.verbose:
            print(
                f"Performing introspection on task: {self.get_value_or_default(graph_state, 'task')}"
            )

        prompt = {
            "instructions": (
                self.instructions
                + " Based on the latest message, guidelines, and task, "
                "provide an improved version of the last message. "
                "Ensure the response adheres to the provided format and guidelines."
                "Always respond in valid JSON format."
            ),
            "task": self.get_value_or_default(graph_state, "task"),
            "reviewer feedback": self.get_value_or_default(graph_state, "feedback"),
            "guidelines": self.get_value_or_default(graph_state, "guidelines"),
            "messages": self.get_value_or_default(graph_state, "messages"),
            "response format": {"message": "Your response here"},
            "examples": {
                "example reponse 1": {
                    "message": "This is a good start, but here is an improved version: ..."
                },
                "example reponse 2": {
                    "message": "You are on the right track, but consider this: ..."
                },
                "example reponse 3": {
                    "message": "Good effort, but try this instead: ..."
                },
                "example reponse 4": {
                    "message": "Almost there, but this is a better version: ..."
                },
            },
        }

        agent_response = self._invoke_model(prompt, "message")

        if self.verbose:
            print(
                f"Introspection suggestion: {self.get_value_or_default(agent_response, 'message')}"
            )

        graph_state["messages"] = self.get_value_or_default(agent_response, "message")
        return graph_state
