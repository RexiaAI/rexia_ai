"""CodeTool class for ReXia.AI"""

import logging
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from typing import Any, List, Dict
from ...base import BaseWorker
from ...structure import RexiaAIResponse
from ...common import ContainerisedToolRunner

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class ToolGenerationError(Exception):
    pass

class ToolExecutionError(Exception):
    pass

PREDEFINED_PROMPT = """
As an AI assistant for ReXia.AI, your task is to implement Python function(s) that will solve the given problem. 
Follow these guidelines:

### Environment
- Python 3.12
- Isolated container with only built-in libraries
- No external libraries, API keys, environment variables, or system-specific features

### Key Points
1. **Use Built-in Libraries**:
   - Use only Python's built-in libraries and functions.
   - Do not import or use any external packages.

2. **Avoid Restricted Operations**:
   - Avoid any operations requiring API keys, network calls, or file operations.

3. **Code Quality**:
   - Implement efficient, Pythonic code with appropriate built-ins.
   - Handle errors and edge cases gracefully.
   - Provide clear docstrings and type hints.

### Style Guidelines
1. **Indentation**:
   - Use 4 spaces for indentation.

2. **Line Length**:
   - Maximum 100 characters per line.

3. **Naming Conventions**:
   - Use snake_case for function and variable names.

4. **Documentation**:
   - Include concise docstrings and type hints.

### Implementation
1. **Function Definitions**:
   - Define the function(s) necessary to solve the given problem.
   - Include necessary import statements only from built-in modules.
   - Implement the required logic using only built-in Python features.

2. **Main Function**:
   - Create a `main()` function that solves the problem and returns the result.

### Output Format
- Provide code in the "answer" field as a list of strings.
- Each string represents one line of code.
- Preserve indentation with EXACTLY 4 spaces per level.
- Include empty lines as empty strings.
- The code will be joined and executed directly.
- It is required that your response has a `main()` function that returns the result or it will fail.

### Example Output Format
```json
{
  "question": "Calculate the sum of all even numbers between 1 and 100, inclusive.",
  "plan": [
    "Define a function to check if a number is even",
    "Define a function to calculate the sum of even numbers in a range",
    "Create a main() function to solve the problem and return the result"
  ],
  "answer": [
    "def is_even(n: int) -> bool:",
    "    return n % 2 == 0",
    "",
    "def sum_even_numbers(start: int, end: int) -> int:",
    "    return sum(num for num in range(start, end + 1) if is_even(num))",
    "",
    "def main() -> int:",
    "    return sum_even_numbers(1, 100)",
    ""
  ],
  "confidence_score": 95.0,
  "chain_of_reasoning": [
    "Define is_even function to check if a number is even",
    "Define sum_even_numbers function to calculate the sum of even numbers in a range",
    "Use list comprehension with is_even check to generate even numbers",
    "Use built-in sum function to calculate the total",
    "Create main() function to call sum_even_numbers with the required range and return the result"
  ],
  "tool_calls": []
}
"",
"def sum_even_numbers(start: int, end: int) -> int:",
"    return sum(num for num in range(start, end + 1) if is_even(num))",
"",
"def main() -> int:",
"    return sum_even_numbers(1, 100)",
""
],
"confidence_score": 95.0,
"chain_of_reasoning": [
"Define is_even function to check if a number is even",
"Define sum_even_numbers function to calculate the sum of even numbers in a range",
"Use list comprehension with is_even check to generate even numbers",
"Use built-in sum function to calculate the total",
"Create main() function to call sum_even_numbers with the required range and return the result"
],
"tool_calls": []
Now, implement the solution for the following problem:
"""

class CodeTool(BaseWorker):
    """
    A worker for ReXia AI that generates Python tools based on given tasks.
    This class extends BaseWorker to provide specialized functionality for
    generating and executing Python code tools using a language model.

    Attributes:
        tool_runner (ContainerisedToolRunner): An instance of ContainerisedToolRunner
        used to execute the generated code in a secure environment.
    """

    def __init__(self, model: Any, verbose: bool = False):
        """
        Initialize a CodeTool instance.

        Args:
            model (Any): The language model to be used for generating code.
            verbose (bool, optional): If True, enables verbose output. Defaults to False.
        """
        super().__init__(model, verbose=verbose)
        self.tool_runner = ContainerisedToolRunner()

    def create_prompt(self, task: str, messages: List[str]) -> str:
        """
        Create a prompt for the language model to generate a Python tool.
        This method constructs a prompt by combining a predefined prompt template
        with the specific task description.

        Args:
            task (str): The task description for which to create a tool.
            messages (List[str]): List of previous messages in the conversation.

        Returns:
            str: The generated prompt for the language model.
        """
        task_prompt = f"""
        Task: {task}
        Implement the necessary Python function(s) to create a tool that retrieves relevant information for this task.
        Information returned by the Python function(s) will be used by a large language model to solve the test.
        Remember to use only built-in Python libraries and avoid any external dependencies or API calls.
        """
        # Combine the predefined prompt with the task-specific prompt
        prompt = super().create_prompt(PREDEFINED_PROMPT + task_prompt, task, messages)
        return prompt

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type((ToolGenerationError, ToolExecutionError)),
        before_sleep=lambda retry_state: logger.info(f"Retrying action (attempt {retry_state.attempt_number})"),
        reraise=True,
    )
    def action(self, prompt: str, worker_name: str) -> str:
        """
        Execute the action of generating and running a Python tool based on the given prompt.
        This method attempts to generate code using the language model, execute it
        in a containerized environment, and handle any errors that occur. It will
        make multiple attempts if the initial code generation or execution fails.

        Args:
            prompt (str): The prompt for generating the tool.
            worker_name (str): The name of the worker executing this action.

        Returns:
            str: A formatted string containing the worker's response and tool execution results.

        Raises:
            RetryError: If all retry attempts fail.
        """
        try:
            agent_response = self._invoke_model(prompt)
            if not isinstance(agent_response, RexiaAIResponse):
                raise ToolGenerationError(f"Expected RexiaAIResponse, got {type(agent_response)}")

            code = self._extract_code(agent_response)
            if self.verbose:
                logger.info("Code to execute:")
                logger.info(code)

            result = self.tool_runner.execute_code(code)
            if result.get("success"):
                output = result.get("output", "No output")
                logger.info(f"Tool execution successful. Output: {str(result)}")
                return self._format_response(worker_name, agent_response, output)
            else:
                error_message = f"Error: {result['error']}"
                if self.verbose:
                    logger.error(error_message)
                # Update the prompt with error information
                prompt = self._update_prompt_with_error(prompt, agent_response, error_message)
                raise ToolExecutionError(error_message)
        except Exception as e:
            logger.error(f"Error during attempt: {str(e)}")
            # Update the prompt with error information
            prompt = self._update_prompt_with_error(prompt, agent_response, str(e))
            raise ToolGenerationError(str(e))

    def _update_prompt_with_error(self, prompt: str, agent_response: RexiaAIResponse, error_message: str) -> str:
        return f"""
        The Python code within the answer field of this JSON object returned an error.
        Original prompt: {prompt}
        JSON Object: {agent_response}
        Error: {error_message}
        Please return the full previous JSON object with the answer updated to fix this error.
        """

    def _extract_code(self, agent_response: RexiaAIResponse) -> str:
        return "\n".join(agent_response.answer) if isinstance(agent_response.answer, list) else agent_response.answer

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