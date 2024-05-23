"""BaseAgent class for ReXia AI."""

import re
import json
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

    def action(self, agency_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Work on the current task."""
        graph_state = agency_state
        return graph_state

    def _strip_control_characters(self, s: str) -> str:
        """Strip control characters from a string."""
        control_char_regex = re.compile(r"[\x00-\x1F\x7F]")
        stripped_string = control_char_regex.sub("", s)

        return stripped_string
    
    def remove_substrings(self, s: str):
        """Remove the start and end substrings from the string."""
        start_substring = "```json"
        end_substring = "```"
        if s.startswith(start_substring):
            s = s[len(start_substring):]  # Remove the start substring
        if s.endswith(end_substring):
            s = s[:-len(end_substring)]  # Remove the end substring
        return s

    def _invoke_model(self, prompt: dict, key: str, max_retries: int = 3) -> dict:
        """Invoke the model with the given prompt and return the response."""
        for k, value in prompt.items():
            if isinstance(value, set):
                prompt[k] = list(value)
        for i in range(max_retries):
            response = self.model.invoke(json.dumps(prompt)).content
            cleaned_response = self._strip_control_characters(response)
            cleaned_response = self.remove_substrings(cleaned_response)
            try:
                json_response = json.loads(cleaned_response)
                while (
                    self.get_value_or_default(json_response, key)
                    == f"No value found for {key}"
                ):
                    print(f"No {key} found, retrying...")
                    if self.verbose:
                        print(f"Response: {cleaned_response}")
                    response = self.model.invoke(json.dumps(prompt)).content
                    cleaned_response = self._strip_control_characters(response)
                    cleaned_response = self.remove_substrings(cleaned_response) 
                    json_response = json.loads(cleaned_response)
                return json_response
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON response: {cleaned_response}")
                if i < max_retries - 1:  # Don't print this message on the last retry
                    print("Invalid JSON response, retrying...")
        print(f"Failed to get a valid response from the model after {max_retries} attempts.")
        return {"message": f"Failed to get a valid response from the model after {max_retries} attempts."}
        
    def get_value_or_default(self, schema: WorkflowStateSchema, key: str) -> str:
        """Get the value for the key from the schema, or return a default message."""
        return schema.get(key, f"No value found for {key}")
