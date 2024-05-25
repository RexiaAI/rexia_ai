"""BaseAgent class for ReXia AI."""

import re
from typing import List, Optional
from langchain_core.tools import Tool
from ..llms import RexiaAIChatOpenAI
from ..common import WorkflowStateSchema


class BaseAgent:
    """BaseAgent for ReXia AI."""

    model: RexiaAIChatOpenAI
    tools: Optional[List[Tool]]

    def __init__(
        self, model: RexiaAIChatOpenAI, instructions: str = "", verbose: bool = False
    ):
        self.model = model
        self.instructions = instructions
        self.verbose = verbose

    def action(self, graph_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Work on the current task."""
        return graph_state

    def remove_system_tokens(self, s: str):
        """Remove system tokens from the string."""
        return re.sub(r"<\|.*\|>", "", s)

    def _invoke_model(self, prompt) -> str:
        """Invoke the model with the given prompt and return the response."""
        response = self.model.invoke(prompt).content
            
        return response
    
    def _clean_response(self, response: str) -> str:
        """Clean the response from the model."""
        cleaned_response = self.remove_system_tokens(response)
        return cleaned_response

    def _create_prompt(
        self, graph_state: WorkflowStateSchema
    ) -> dict:
        """Create a prompt for a task."""
        prompt = f"""role: You are a helpful agent. You read the task, guidelines, messages and feeddback
            and generate a completion of the task. You always listen to feedback. You always follow the guidelines
            step by step.\n\n
            task: {graph_state["task"]},\n\n
            feedback: {graph_state["feedback"]},\n\n
            guidelines: {graph_state["guidelines"]},\n\n
            instructions: {self.instructions}"""

        return prompt