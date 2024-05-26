"""WorkAgent class for ReXia AI."""

from typing import List, Optional
from langchain_core.tools import Tool
from ..llms import ReXiaAIChatOpenAI
from ..common import WorkflowStateSchema
from ..base import BaseAgent


class WorkAgent(BaseAgent):
    """WorkAgent for ReXia AI."""

    model: ReXiaAIChatOpenAI
    tools: Optional[List[Tool]]

    def __init__(
        self, model: ReXiaAIChatOpenAI, instructions: str = "", verbose: bool = False
    ):
        super().__init__(model, instructions=instructions, verbose=verbose)

    def action(self, graph_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Work on the current task."""

        if self.verbose:
            print(
                f"Worker working on task: {graph_state['task']}"
            )

        prompt = self._create_prompt(graph_state)

        agent_response = self._invoke_model(prompt)

        if self.verbose:
            print(
                f"Worker response: {agent_response}"
            )

        graph_state["messages"].append(agent_response)
        return graph_state
