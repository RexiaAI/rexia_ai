"""BaseAgent class for ReXia AI."""

import re
from typing import Any
from ..structure import LLMOutput


class BaseWorker:
    """BaseAgent for ReXia AI."""

    def __init__(self, model: Any, verbose: bool = False):
        self.model = model
        self.verbose = verbose

    def action(
        self,
        prompt: str,
        worker_name: str,
    ) -> str:
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
        cleaned_response = self._strip_python_tags(cleaned_response)
        return cleaned_response

    def _strip_python_tags(self, code: str) -> str:
        """Strip python tags from the start and end of a string of code."""
        return re.sub(r"^```python\n|```$", "", code, flags=re.MULTILINE)

    def get_structured_output_prompt(self):
        """Get the structured output prompt."""
        return f"""Structure your response using the following format, include no information outside this structure:
                {LLMOutput.get_output_structure()}
                """

    def get_plan_structured_output_prompt(self):
        """Get the structured output prompt for planning."""
        return f"""Structure your response using the following format, include no information outside this structure:
                {LLMOutput.get_plan_output_structure()}
                """

    def get_approval_structured_output_prompt(self):
        """Get the structured output prompt for approval."""
        return f"""Structure your response using the following format, include no information outside this structure:
                {LLMOutput.get_approval_output_structure()}
                """
