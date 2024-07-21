"""ToolWorker class for ReXia.AI's tool interaction and management system."""

import logging
from typing import Any, List, Dict
from ...base import BaseWorker
from ...structure import RexiaAIResponse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


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
    A specialized tool worker for ReXia.AI's agent system, focused on tool interaction and management.

    This worker is responsible for selecting appropriate tools, making tool calls,
    processing their outputs, and integrating results into the overall task solution.
    It plays a crucial role in enhancing the problem-solving capabilities of ReXia.AI
    by leveraging external tools and APIs effectively.

    Attributes:
        model (Any): The language model used for processing prompts and making decisions about tool usage.
        verbose (bool): Flag for enabling verbose output mode.

    Inherits from:
        BaseWorker: Provides core functionality for AI workers in the ReXia.AI system.
    """

    def __init__(self, model: Any, verbose: bool = False):
        """
        Initialize a ToolWorker instance.

        Args:
            model (Any): The language model to be used for processing and decision-making.
            verbose (bool, optional): Enable verbose output for debugging. Defaults to False.
        """
        super().__init__(model, verbose=verbose)
        logger.info("ToolWorker initialized")

    def action(self, prompt: str, worker_name: str) -> str:
        """
        Execute the main action for the current task based on the provided prompt.

        This method processes the prompt, makes necessary tool calls, and formats the final response.

        Args:
            prompt (str): The input prompt containing task details and context.
            worker_name (str): Identifier for the worker executing this action.

        Returns:
            str: Formatted response including tool call results and any additional insights.
        """
        logger.info(f"Executing action for worker: {worker_name}")
        agent_response = self._invoke_model(prompt)
        results = self._handle_tool_calls(agent_response)
        return self._format_response(worker_name, agent_response, results)

    def create_prompt(self, task: str, messages: List[str], memory: Any) -> str:
        """
        Construct a detailed prompt for the model incorporating task details, context, and available tools.

        This method combines the predefined prompt with task-specific information, conversation history,
        and a list of available tools to create a comprehensive prompt for the model.

        Args:
            task (str): The current task or problem statement.
            messages (List[str]): Previous messages or context relevant to the task.
            memory (Any): Additional context or information stored in the agent's memory.

        Returns:
            str: A formatted prompt string for the model to guide tool selection and usage.
        """
        logger.info("Creating prompt for task")
        prompt = super().create_prompt(PREDEFINED_PROMPT, task, messages, memory)
        prompt += f"\n\nAvailable Tools:\n{self._get_available_tools()}\n\n"
        return prompt

    def _handle_tool_calls(self, rexia_ai_response: RexiaAIResponse) -> Dict[str, Any]:
        """
        Process and execute tool calls specified in the model's response.

        This method iterates through tool calls, validates tool availability, executes
        tool functions, and handles any errors or exceptions during the process.

        Args:
            rexia_ai_response (RexiaAIResponse): The response object containing tool calls to be processed.

        Returns:
            Dict[str, Any]: A dictionary mapping tool names to their execution results or error messages.
        """
        results = {}
        logger.info(f"Processing {len(rexia_ai_response.tool_calls)} tool calls")
        for tool_call in rexia_ai_response.tool_calls:
            tool_name = tool_call.get("name")
            tool_args = tool_call.get("parameters", {})
            logger.debug(f"Processing tool call: {tool_name}")

            if tool_name not in self.model.tools:
                logger.warning(f"Tool not found: {tool_name}")
                results[tool_name] = f"Error: Tool {tool_name} not found."
                continue

            tool = self.model.tools[tool_name]
            function_name = tool.to_rexiaai_function_call().get("name")
            function_to_call = getattr(tool, function_name, None)

            if not function_to_call:
                logger.error(f"Function {function_name} not found in tool {tool_name}")
                results[tool_name] = (
                    f"Error: Function {function_name} not found in tool {tool_name}"
                )
                continue

            try:
                results[tool_name] = function_to_call(**tool_args)
                logger.info(f"Successfully executed {function_name} in {tool_name}")
            except Exception as e:
                logger.exception(f"Error executing {function_name} in {tool_name}: {str(e)}")
                results[tool_name] = (
                    f"Error executing {function_name} in {tool_name}: {str(e)}"
                )

        return results

    def _format_response(
        self, worker_name: str, agent_response: str, results: Dict
    ) -> str:
        """
        Format the final response including worker identification, raw agent response, and tool call results.

        If verbose mode is enabled, this method also prints a detailed response for debugging purposes.

        Args:
            worker_name (str): Identifier for the worker formatting the response.
            agent_response (str): The raw response generated by the agent.
            results (Dict): Results of the tool calls made during the action.

        Returns:
            str: A formatted string containing the worker's response and tool call results.
        """
        formatted_response = f"{worker_name}: {results}"
        if self.verbose:
            logger.debug(f"Verbose output: {worker_name}: {agent_response}\n\nTool messages: {results}")
        return formatted_response

    @staticmethod
    def _format_messages(messages: List[str]) -> str:
        """
        Format a list of messages into a single string for display or further processing.

        Args:
            messages (List[str]): A list of message strings to be formatted.

        Returns:
            str: A single string with messages joined by double newlines.
        """
        formatted = "\n\n".join(messages)
        return formatted