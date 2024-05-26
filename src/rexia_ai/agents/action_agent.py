"""WorkAgent class for ReXia AI."""

from typing import List, Optional
from langchain_core.tools import Tool
from ..llms import ReXiaAIChatOpenAI
from ..common import WorkflowStateSchema
from ..base import BaseAgent


class ActionAgent(BaseAgent):
    """WorkAgent for ReXia AI."""

    model: ReXiaAIChatOpenAI
    tools: Optional[List[Tool]]

    def __init__(
        self, model: ReXiaAIChatOpenAI, instructions: str = "", verbose: bool = False
    ):
        super().__init__(model, instructions=instructions, verbose=verbose)
        self.name = "Actor"

    def action(self, graph_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Work on the current task."""

        if self.verbose:
            print(
                f"Act being performed for task: {graph_state['task']}"
            )

        prompt = self._create_prompt(graph_state)

        agent_response = self._invoke_model(prompt)

        if self.verbose:
            print(agent_response)

        graph_state["messages"].append(agent_response)
        return graph_state
    
    def _create_prompt(self, graph_state: WorkflowStateSchema) -> dict:
        """Create a prompt for a action task."""
        prompt = f"""role: You are a helpful assistant, read the messages for the latest
                thought and take the action it suggests.\n\n
                task: {graph_state["task"]},\n\n
                messages: {graph_state["messages"]},\n\n
                respond in this format:
                    action: the action you have taken and the result of that action.
                """
        return prompt

