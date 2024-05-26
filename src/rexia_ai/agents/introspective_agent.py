"""IntrospectriveAgent class for ReXia AI."""

from typing import List, Optional
from langchain_core.tools import Tool
from ..llms import ReXiaAIChatOpenAI
from ..common import WorkflowStateSchema
from ..base import BaseAgent


class IntrospectiveAgent(BaseAgent):
    """IntrospectiveAgent for ReXia AI."""

    model: ReXiaAIChatOpenAI
    tools: Optional[List[Tool]]

    def __init__(
        self, model: ReXiaAIChatOpenAI, instructions: str = "", verbose: bool = False
    ):
        super().__init__(model, instructions=instructions, verbose=verbose)

    def action(self, graph_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Perform introspection on the current task."""

        if self.verbose:
            print(
                f"Performing introspection on task: {graph_state['task']}"
            )

        prompt = self._create_prompt(graph_state)

        agent_response = self._invoke_model(prompt)

        if self.verbose:
            print(
                f"Introspection suggestion: {agent_response}"
            )

        graph_state["messages"] = agent_response
        return graph_state

    def _create_prompt(self, graph_state: WorkflowStateSchema) -> dict:
        """Create a prompt for introspection on a task."""
        prompt = f"""
            task: {graph_state["task"]}\n\n
            feedback: {graph_state["feedback"]}\n\n
            guidelines: {graph_state["guidelines"]}\n\n
            messages: {graph_state["messages"]}\n\n
            instructions:\n
                Based on the latest message, guidelines, feedback and task,
                provide an improved version of the last message.
                Follow the guidelines step by step.
                Listen to feedback and adjust the message accordingly.
                Respond with nothing but the improved message.
        """

        return prompt
