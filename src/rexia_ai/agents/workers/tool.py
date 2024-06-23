"""ToolWorker class in ReXia.AI."""

from typing import Any, List, Dict
from ...base import BaseWorker
from ...structure import RexiaAIResponse

PREDEFINED_PROMPT = """
        As a tool calling agent for ReXia.AI, your role is key in supporting task completion. 

        Select tools based on their capabilities, limitations, and trade-offs. Aim for efficiency and minimal redundancy.

        Use tools wisely. Make multiple calls if needed, refining your approach based on previous outputs.
        Always make at least one tool call to contribute to the solution.

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
        
        Ignore any existing tool calls in the collaboration chat and make your own.

        {
        "tool_calls": [
            {
            "name": "ToolName",
            "parameters": {
                "parameter1": "value1",
                "parameter2": "value2"
            }
            }
        ]
        }

        For example, if asked "What is 3 * 12?" and you have a Multiply tool, respond with:

        {
        "tool_calls": [
            {
            "name": "Multiply",
            "parameters": {
                "a": 3,
                "b": 12
            }
            }
        ]
        }
        """


class ToolWorker(BaseWorker):
    """
    A specialized tool worker for ReXia.AI agents, responsible for handling tool-related actions.

    This worker is designed to interact with various tools to gather information or perform actions
    that assist in completing tasks assigned to the ReXia.AI agent. It manages tool calls, processes
    their outputs, and integrates these results into the agent's workflow.

    Attributes:
        model (Any): The model used by the worker for making tool calls and processing responses.
        verbose (bool): If True, enables detailed logging of actions and responses for debugging.
        max_attempts (int): The maximum number of attempts to make for a valid response from a tool.
    """

    def __init__(self, model: Any, verbose: bool = False, max_attempts: int = 3):
        """
        Initializes a ToolWorker instance with a model, verbosity setting, and maximum attempt limit.

        Args:
            model (Any): The model instance to be used by the ToolWorker for processing and tool interaction.
            verbose (bool): Flag to enable verbose output. Useful for debugging. Defaults to False.
            max_attempts (int): Maximum number of attempts to get a valid response from the model. Defaults to 3.
        """
        super().__init__(model, verbose=verbose, max_attempts=max_attempts)

    def action(self, prompt: str, worker_name: str) -> str:
        """
        Executes the main action for the current task based on the provided prompt.

        This method invokes the model with the prompt, handles the tool calls in the model's response,
        and formats the final response.

        Args:
            prompt (str): The prompt to be processed by the model.
            worker_name (str): The name of the worker performing the action.

        Returns:
            str: The formatted response after processing the prompt and tool calls.
        """
        agent_response = self._invoke_model(prompt)
        results = self._handle_tool_calls(agent_response)
        return self._format_response(worker_name, agent_response, results)

    def create_prompt(self, task: str, messages: List[str], memory: Any) -> str:
        """
        Constructs a detailed prompt for the model based on the task, previous messages, and memory.

        This method prepares a comprehensive prompt that includes the predefined prompt, available tools,
        and any additional context necessary for the model to generate a response.

        Args:
            task (str): The current task description.
            messages (List[str]): Previous messages in the conversation for context.
            memory (Any): Additional memory or context that might be relevant to the task.

        Returns:
            str: The constructed prompt for the model.
        """
        prompt = super().create_prompt(PREDEFINED_PROMPT, task, messages, memory)

        prompt = prompt + f"\n\nAvailable Tools:\n{self._get_available_tools()}\n\n"

        return prompt

    def _handle_tool_calls(self, rexia_ai_response: RexiaAIResponse) -> Dict[str, Any]:
        """
        Processes and executes tool calls found in the RexiaAIResponse object.

        This method iterates through tool calls, checks for tool availability, and executes the tool's
        function with the provided arguments. It handles errors and exceptions during tool execution.

        Args:
            rexia_ai_response (RexiaAIResponse): The response object containing tool calls to process.

        Returns:
            Dict[str, Any]: A dictionary with tool names as keys and their execution results or error messages as values.
        """
        results = {}
        for tool_call in rexia_ai_response.tool_calls:
            tool_name = tool_call.get("name")
            tool_args = tool_call.get("parameters", {})

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
        """
        Formats the final response including the worker name, the raw agent response, and the results of tool calls.

        If verbose mode is enabled, this method also prints the detailed response.

        Args:
            worker_name (str): The name of the worker.
            agent_response (str): The raw response from the agent.
            results (Dict): The results of the tool calls.

        Returns:
            str: The formatted final response.
        """
        if self.verbose:
            print(f"{worker_name}: {agent_response}\n\nTool messages: {results}")
        return f"{worker_name}: {results}"

    @staticmethod
    def _format_messages(messages: List[str]) -> str:
        """
        Formats a list of messages for display or further processing.

        This method joins a list of messages into a single string, separated by double newlines.

        Args:
            messages (List[str]): The messages to format.

        Returns:
            str: The formatted string of messages.
        """
        return "\n\n".join(messages)
