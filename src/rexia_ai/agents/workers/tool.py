"""ToolWorker class in ReXia.AI."""
import json
import secrets
import re
from typing import List, Dict, Tuple
from ...base import BaseWorker
from ...llms import RexiaAIOpenAI

PREDEFINED_PROMPT = """
You are a function calling agent for the ReXia.AI system, an advanced AI
platform designed to tackle complex tasks and problems. Your role is crucial in
gathering the necessary information and resources to support the team in
completing the given task effectively and efficiently.

When selecting tools, consider their capabilities, limitations, and potential
trade-offs. Choose the most appropriate tools that can provide the required
information while minimizing redundancy and optimizing the overall process.

Use the tools efficiently and avoid unnecessary or redundant tool calls. You
can make multiple tool calls based on the output of previous tool calls,
iteratively refining your approach and gathering more targeted information as
needed.

After calling a tool, carefully handle and interpret its output. Parse the
output, handle errors or edge cases, and incorporate the tool output into the
overall solution. If a tool's output is unclear or insufficient, consider
calling additional tools or seeking clarification from the team.

Remember, you are part of a collaborative team. Communicate effectively with
other team members, share relevant information, and coordinate your efforts to
ensure a cohesive and efficient approach to the task.

Be mindful of potential limitations or constraints, such as resource
constraints, time constraints, or ethical considerations, and adjust your tool
selection and usage accordingly.

To call a tool, use the JSON format provided below, ensuring that your tool
calls are properly formatted JSON with the correct tool names and arguments.
Do not generate incomplete JSON or JSON with syntax errors. 
"""

class ToolWorker(BaseWorker):
    """
    A specialised tool writing worker for a ReXia.AI agent.

    This worker is responsible for gathering information for the rest of the team to complete the task.

    Attributes:
        model: The model used by the worker.
    """

    model: RexiaAIOpenAI

    def __init__(
        self,
        model: RexiaAIOpenAI,
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
    
    def _handle_tool_calls(self, data: Dict) -> Dict:
        """
        Handle the tool calls in the data.

        Args:
            data: The data containing the tool calls.

        Returns:
            The results of the tool calls as a dictionary.
        """
        results = {}

        if "tool_calls" in data:
            for tool_call in data["tool_calls"]:
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args", {})
                tool_id = tool_call.get("id")

                if tool_name in self.model.tools:
                    tool = self.model.tools[tool_name]
                    function_name = tool.to_rexiaai_function_call().get("name")
                    function_to_call = getattr(tool, function_name, None)
                    if function_to_call:
                        try:
                            result = function_to_call(**tool_args)
                            results[tool_id] = result
                        except Exception as e:
                            results[tool_id] = str(e)
                    else:
                        print(f"Function {function_name} not found in tool {tool_name}")
                else:
                    print(f"Tool {tool_name} not found")
                    print("\n\nAvailable tools: \n")
                    for tool in self.model.tools:
                        print(str(tool) + "\n")

        return results
    
    def _extract_and_parse_json(self, agent_response: str) -> Tuple[str, Dict]:
        """
        Parse the agent response as JSON.

        Args:
            agent_response: The response from the agent.

        Returns:
            The JSON part of the agent response and the parsed data as a dictionary.
        """
        for _ in range(3):
            try:
                # Extract JSON part using a regular expression
                json_match = re.search(r"\{.*\}", agent_response, re.DOTALL)
                if json_match:
                    json_part = json_match.group()
                    data = json.loads(json_part)
                    return agent_response, data
            except json.JSONDecodeError:
                print("Could not parse JSON. Retrying...")

        print("Failed to parse JSON after 3 attempts")
        return agent_response, {}
    
    def _format_response(
    self, worker_name: str, agent_response: str, results: Dict
    ) -> str:
        """
        Format the response.

        Args:
            worker_name: The name of the worker.
            agent_response: The response from the agent.
            results: The results of the tool calls.

        Returns:
            The formatted response as a string.
        """
        if self.verbose:
            print(f"{worker_name}: {agent_response}\n\n Results: {results}")

        return f"{worker_name}: {results}"

    def _get_unique_id(self) -> str:
        """
        Get a unique id.

        Returns:
            The unique id as a string.
        """
        return secrets.token_hex(16)