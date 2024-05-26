"""CodeWorkAgent class for ReXia AI."""

from typing import List, Optional
from langchain_core.tools import Tool
from ..llms import ReXiaAIChatOpenAI
from ..common import WorkflowStateSchema
from ..base import BaseAgent


class CodeWorkAgent(BaseAgent):
    """CodeWorkAgent for ReXia AI. A worker agent specialised in coding tasks."""

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
    
    def _create_prompt(self, graph_state: WorkflowStateSchema) -> dict:
        """Create a prompt for a coding task."""
        prompt = f"""role: You are a senior developer. You read the task, guidelines, messages, and feeddback
            and generate code that represents a completion of the task. You always listen to feedback.
            Ensure that code you write adheres to industry best practices, including readability, efficiency, and 
            security measures. The code you generate should be easily maintainable and understandable, incorporating error
            handling and relevant comments to explain the logic and functionality.
            You always follow the guidelines step by step. 
            Only respond with code. \n\n
            Format:\n
                Start with a brief comment summarizing the purpose of the code.
                Follow best practices for the specified programming language regarding syntax, naming conventions, and structure.
                Include inline comments to explain complex or critical parts of the code.
                Ensure the code is structured in a way that supports easy testing and debugging.
            task: {graph_state["task"]},\n\n
            feedback: {graph_state["feedback"]},\n\n
            guidelines: {graph_state["guidelines"]},\n\n
            instructions: {self.instructions}"""

        return prompt
