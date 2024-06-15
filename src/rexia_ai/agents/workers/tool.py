"""ToolWorker class in ReXia.AI."""

from typing import List
from ...base import BaseWorker
from ...llms import LLM

PREDEFINED_PROMPT = """
***Role: Tool Agent***
    You are a function calling agent.
    You are part of a team working on a task.
    Read the collaboration chat and the task fully to understand the context.
    Your job is to gather information for the rest of the team to complete the task.
    You have several available tools to help you.
    Please select the most appropriate tools to use and call them with the correct parameters.
    Use the tools by calling them using the JSON format below format:    
"""

class ToolWorker(BaseWorker):
    """
    A specialised tool writing worker for a ReXia.AI agent.

    This worker is responsible for gathering information for the rest of the team to complete the task.

    Attributes:
        model: The model used by the worker.
    """

    model: LLM

    def __init__(
        self,
        model: LLM,
        verbose: bool = False,
    ):
        """
        Initialize a ToolWorker instance.

        Args:
            model: The model used by the worker.
            verbose: A flag used for enabling verbose mode. Defaults to False.
        """
        super().__init__(model, verbose=verbose)

    def action(self, prompt: str, worker_name: str) -> str:
        """
        Work on the current task.

        Args:
            prompt: The prompt for the model.
            worker_name: The name of the worker.

        Returns:
            The formatted response from the model.
        """
        agent_response = self._invoke_model(prompt)
        json_part, data = self._extract_and_parse_json(agent_response)
        results = self._handle_tool_calls(data)
        formatted_response = self._format_response(worker_name, agent_response, results)
        return formatted_response

    def create_prompt(self, task: str, messages: List[str]) -> str:
        """
        Create a prompt for the model.

        The prompt is created by combining a predefined string with the task
        and the messages from the collaboration chat.

        Args:
            task: The task for which the prompt is created.
            messages: The messages from the collaboration chat.

        Returns:
            The created prompt as a string.
        """
        unique_id = self._get_unique_id()

        prompt = (
            PREDEFINED_PROMPT
            + """
                {
                "tool_calls": [
                    {
                    "name": "ToolName",
                    "args": {
                        "arg1": "value1",
                        "arg2": "value2"
                    },
                    "id": "{unique_id}"
                    }
                ]
                }

                For example, if asked "What is 3 * 12?", respond with:

                {
                "tool_calls": [
                    {
                    "name": "Multiply",
                    "args": {
                        "a": 3,
                        "b": 12
                    },
                    "id": "{unique_id}"
                    }
                ]
                }
            
            Ensure your tool calls are properly formatted JSON and that you use the correct tool names and arguments.
            Do not generate incomplete JSON or JSON with syntax errors.
            """
            + f"""
            Task: {task}

            Available Tools:
            {self._get_available_tools()}

            Collaboration Chat:
            """
            + "\n\n".join(messages)
        ).replace("{unique_id}", unique_id)

        return prompt