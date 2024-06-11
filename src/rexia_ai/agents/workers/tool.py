"""ToolWorker class for ReXia AI."""

import json
import re
import secrets
from typing import List, Dict, Tuple
from ...base import BaseWorker
from ...llms import LLM


class ToolWorker(BaseWorker):
    """A specialised tool writing worker for a ReXia AI agent."""

    model: LLM

    def __init__(
        self,
        model: LLM,
        verbose: bool = False,
    ):
        super().__init__(model, verbose=verbose)
        
    def action(self, prompt: str, worker_name: str) -> str:
        """Work on the current task."""
        agent_response = self._invoke_model(prompt)
        json_part, data = self._extract_and_parse_json(agent_response)
        results = self._handle_tool_calls(data)
        return self._format_response(worker_name, agent_response, results)


    def create_prompt(self, task: str, messages: List[str]) -> str:
        """Create a prompt for the model."""
        unique_id = self._get_unique_id()
        
        prompt = (
            """
            ***Role: Tool Agent***
                You are a function calling agent.
                You are part of a team working on a task.
                Read the collaboration chat and the task fully to understand the context.
                Your job is to gather information for the rest of the team to complete the task.
                You have several available tools to help you.
                Please select the most appropriate tools to use and call them with the correct parameters.
                Use the tools by calling them using the JSON format below format:    
            """ + """
                                
                {
                "tool_calls": [
                    {
                    "name": "ToolName",
                    "args": {
                        "arg1": "value1",
                        "arg2": "value2"
                    },
                    "id": "UNIQUE_ID_PLACEHOLDER"
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
                    "id": "UNIQUE_ID_PLACEHOLDER"
                    }
                ]
                }
            """ +
            f"""
            Task: {task}

            Available Tools:
            {self._get_available_tools()}

            Collaboration Chat:
            """
            + "\n\n".join(messages)
        )
        prompt = prompt.replace("UNIQUE_ID_PLACEHOLDER", unique_id)
        
        return prompt
    
    def _get_available_tools(self):
        """Get the available tools."""
        tools = ""
        for tool_name, tool in self.model.tools.items():
            tools = tools + f"Tool: {tool_name}, Object: {tool.to_rexiaai_tool()}, Function Call: {tool.to_rexiaai_function_call()}\n"
        
        return tools

    def _extract_and_parse_json(self, agent_response: str) -> Tuple[str, Dict]:
        """Parse the agent response as JSON."""
        try:
            # Extract JSON part using a regular expression
            json_match = re.search(r'\{.*\}', agent_response, re.DOTALL)
            if json_match:
                json_part = json_match.group()
                data = json.loads(json_part)
            else:
                print("Could not find JSON part")
                data = {}
        except json.JSONDecodeError:
            print("Could not parse JSON part")
            data = {}

        return agent_response, data

    def _handle_tool_calls(self, data: Dict) -> Dict:
        """Handle the tool calls in the data."""

        results = {}

        if 'tool_calls' in data:
            for tool_call in data['tool_calls']:
                tool_name = tool_call.get('name')
                tool_args = tool_call.get('args', {})
                tool_id = tool_call.get('id')

                if tool_name in self.model.tools:
                    tool = self.model.tools[tool_name]
                    function_name = tool.to_rexiaai_function_call().get('name')
                    function_to_call = getattr(tool, function_name, None)
                    if function_to_call:
                        results[tool_id] = function_to_call(**tool_args)
                    else:
                        print(f"Function {function_name} not found in tool {tool_name}")
                else:
                    print(f"Tool {tool_name} not found")
                    print("\n\nAvailable tools: \n")
                    for tool in self.model.tools:
                        print(str(tool) + "\n")

        return results

    def _format_response(self, worker_name: str, agent_response: str, results: Dict) -> str:
        """Format the response."""
        if self.verbose:
            print(f"{worker_name}: {agent_response}\n\n Results: {results}")

        return f"{worker_name}: " + f"{results}"
    
    def _get_unique_id(self):
        """Get a unique id."""
        return secrets.token_hex(16)
        