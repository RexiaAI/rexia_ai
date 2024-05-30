"""BaseAgent class for ReXia AI."""

import re
from typing import List, Optional
from langchain_core.tools import Tool
from ..llms import ReXiaAIChatOpenAI


class BaseWorker:
    """BaseAgent for ReXia AI."""

    model: ReXiaAIChatOpenAI
    tools: Optional[List[Tool]]

    def __init__(
        self, model: ReXiaAIChatOpenAI, verbose: bool = False
    ):
        self.model = model
        self.verbose = verbose

    def action(self, prompt: str, worker_name: str,) -> str:
        """Work on the current task."""

        agent_response = self._invoke_model(prompt)

        if self.verbose:
            print(f"{worker_name}: {agent_response}")

        return f"{worker_name}: " + agent_response

    def remove_system_tokens(self, s: str):
        """Remove system tokens from the string."""
        return re.sub(r"<\|.*\|>", "", s)

    def _invoke_model(self, prompt) -> str:
        """Invoke the model with the given prompt and return the response."""
        response = self.model.invoke(prompt).content
        response = self._clean_response(response)
            
        return response
    
    def _clean_response(self, response: str) -> str:
        """Clean the response from the model."""
        cleaned_response = self.remove_system_tokens(response)
        return cleaned_response