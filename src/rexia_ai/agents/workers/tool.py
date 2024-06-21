"""ToolWorker class in ReXia.AI."""

from typing import Any, List, Dict
from ...base import BaseWorker
from ...structure import RexiaAIResponse

PREDEFINED_PROMPT = """
        As a tool calling agent for ReXia.AI, your role is key in supporting task completion. 

        Select tools based on their capabilities, limitations, and trade-offs. Aim for efficiency and minimal redundancy.

        Use tools wisely. Make multiple calls if needed, refining your approach based on previous outputs.

        After a tool call, parse the output, handle errors, and integrate the results into the solution. 
        If output is unclear, consider using additional tools or asking the team for clarification.

        Communicate effectively with the team, share important information, and coordinate your efforts for a unified approach.

        Be aware of limitations like resource and time constraints, or ethical considerations, and adjust 
        your tool usage accordingly.

        If the task has specific formatting requests, apply them only within the answer.

        To call a tool, use the JSON format provided below, ensuring that your tool
        calls are properly formatted JSON with the correct tool names and arguments.
        Do not generate incomplete JSON or JSON with syntax errors.
        
        Your tool calls should all be contained within the "tool_calls" list of the
        structured format requested below.

        {
        "tool_calls": [
            {
            "name": "ToolName",
            "args": {
                "arg1": "value1",
                "arg2": "value2"
            }
            }
        ]
        }

        For example, if asked "What is 3 * 12?" and you have a Multiply tool, respond with:

        {
        "tool_calls": [
            {
            "name": "Multiply",
            "args": {
                "a": 3,
                "b": 12
            }
            }
        ]
        }
        """


class ToolWorker(BaseWorker):
    """
    A specialized tool writing worker for a ReXia.AI agent.

    This worker is responsible for gathering information for the rest of the team to
    complete the task.
    """

    def __init__(self, model: Any, verbose: bool = False):
        """Initialize a ToolWorker instance."""
        super().__init__(model, verbose=verbose)

    def action(self, prompt: str, worker_name: str) -> str:
        """Work on the current task."""
        agent_response = self._invoke_model(prompt)
        results = self._handle_tool_calls(agent_response)
        return self._format_response(worker_name, agent_response, results)

    def create_prompt(self, task: str, messages: List[str], memory: Any) -> str:
        """Create a prompt for the model."""
        
        # We can't compress this or the LLM will not understand it needs to call tools.
        prompt = PREDEFINED_PROMPT
        
        prompt = prompt + self._format_additional_context(task, messages, memory)

        prompt = prompt + f"\n\nAvailable Tools:\n{self._get_available_tools()}\n\n"

        return prompt

    def _handle_tool_calls(self, rexia_ai_response: RexiaAIResponse) -> Dict[str, Any]:
        """Handle the tool calls in the rexia_ai_response."""
        results = {}
        for tool_call in rexia_ai_response.tool_calls:
            tool_name = tool_call.get("name")
            tool_args = tool_call.get("args", {})

            if tool_name not in self.model.tools:
                results[tool_name] = f"Error: Tool {tool_name} not found."
                continue

            tool = self.model.tools[tool_name]
            function_name = tool.to_rexiaai_function_call().get("name")
            function_to_call = getattr(tool, function_name, None)

            if not function_to_call:
                results[tool_name] = (
                    f"Error: Function {function_name} not found in tool {tool_name}"
                )
                continue

            try:
                results[tool_name] = function_to_call(**tool_args)
            except Exception as e:
                results[tool_name] = (
                    f"Error executing {function_name} in {tool_name}: {str(e)}"
                )

        return results

    def _format_response(
        self, worker_name: str, agent_response: str, results: Dict
    ) -> str:
        """Format the response."""
        if self.verbose:
            print(f"{worker_name}: {agent_response}\n\nTool messages: {results}")
        return f"{worker_name}: {results}"

    @staticmethod
    def _format_messages(messages: List[str]) -> str:
        """Format the collaboration chat messages."""
        return "\n\n".join(messages)
