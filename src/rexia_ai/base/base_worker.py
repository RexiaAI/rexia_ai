"""BaseWorker class for ReXia.AI."""

import re
from typing import Any
from ..structure import LLMOutput

class BaseWorker:
    """
    BaseWorker for ReXia AI.

    Attributes:
        model: The model used by the worker.
        verbose: A flag used for enabling verbose mode.
    """
    def __init__(self, model: Any, verbose: bool = False):
        """
        Initialize a BaseWorker instance.

        Args:
            model: The model used by the worker.
            verbose: A flag used for enabling verbose mode. Defaults to False.
        """
        self.model = model
        self.verbose = verbose

    def action(self, prompt: str, worker_name: str) -> str:
        """
        Perform an action based on the prompt and return the response.

        Args:
            prompt: The prompt for the action.
            worker_name: The name of the worker performing the action.

        Returns:
            The response from the action.
        """
        agent_response = self._invoke_model(prompt)

        if self.verbose:
            print(f"{worker_name}: {agent_response}")

        return f"{worker_name}: {agent_response}"

    def remove_system_tokens(self, s: str) -> str:
        """
        Remove system tokens from the string.

        Args:
            s: The string from which to remove system tokens.

        Returns:
            The string with system tokens removed.
        """
        return re.sub(r"<\|.*\|>", "", s)

    def _invoke_model(self, prompt: str) -> str:
        """
        Invoke the model with the given prompt and return the response.

        Args:
            prompt: The prompt for the model.

        Returns:
            The response from the model.
        """
        response = self.model.invoke(prompt).content
        response = self._clean_response(response)
        return response

    def _clean_response(self, response: str) -> str:
        """
        Clean the response from the model.

        Args:
            response: The response from the model.

        Returns:
            The cleaned response.
        """
        cleaned_response = self.remove_system_tokens(response)
        cleaned_response = self._strip_python_tags(cleaned_response)
        return cleaned_response

    def _strip_python_tags(self, code: str) -> str:
        """
        Strip python tags from the start and end of a string of code.

        Args:
            code: The code from which to strip python tags.

        Returns:
            The code with python tags stripped.
        """
        return re.sub(r"^```python\n|```$", "", code, flags=re.MULTILINE)

    def get_structured_output_prompt(self) -> str:
        """
        Get the structured output prompt.

        Returns:
            The structured output prompt.
        """
        return f"""Structure your response using the following format, include no information outside this structure:
                {LLMOutput.get_output_structure()}
                """

    def get_plan_structured_output_prompt(self) -> str:
        """
        Get the structured output prompt for planning.

        Returns:
            The structured output prompt for planning.
        """
        return f"""Structure your response using the following format, include no information outside this structure:
                {LLMOutput.get_plan_output_structure()}
                """

    def get_approval_structured_output_prompt(self) -> str:
        """
        Get the structured output prompt for approval.

        Returns:
            The structured output prompt for approval.
        """
        return f"""Structure your response using the following format, include no information outside this structure:
                {LLMOutput.get_approval_output_structure()}
                """

    def _get_available_tools(self) -> str:
        """
        Get the available tools.

        Returns:
            A string representation of the available tools.
        """
        tools = ""
        for tool_name, tool in self.model.tools.items():
            tools += f"Tool: {tool_name}, Object: {tool.to_rexiaai_tool()}, Function Call: {tool.to_rexiaai_function_call()}\n"

        return tools