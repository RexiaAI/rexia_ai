"""WorkAgent class for ReXia AI."""

from typing import List, Optional
from langchain_core.tools import Tool
from ..llms import ReXiaAIChatOpenAI
from ..common import WorkflowStateSchema
from ..base import BaseAgent


class ThoughtAgent(BaseAgent):
    """WorkAgent for ReXia AI."""

    model: ReXiaAIChatOpenAI
    tools: Optional[List[Tool]]

    def __init__(
        self, model: ReXiaAIChatOpenAI, instructions: str = "", verbose: bool = False
    ):
        super().__init__(model, instructions=instructions, verbose=verbose)
        self.name = "Thinker"

    def action(self, graph_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Work on the current task."""

        if self.verbose:
            print(
                f"Thinking about task: {graph_state['task']}"
            )

        prompt = self._create_prompt(graph_state)

        agent_response = self._invoke_model(prompt)

        if self.verbose:
            print(
                agent_response
            )

        graph_state["messages"].append(agent_response)
        return graph_state
    
    def _create_prompt(self, graph_state: WorkflowStateSchema) -> dict:
        """Create a prompt for a thought task."""
        prompt = f"""role: You are a helpful AI assistant, consider your available information and decide the next action
                to take. Only consider actions you could take yourself. 
                If you have tools available, a use of an available tool constitutes a complete action.\n\n
                task: {graph_state["task"]},\n\n
                messages: {graph_state["messages"]},\n\n
                respond in this format:
                    thought: the next action that should be taken.
                """
        return prompt
