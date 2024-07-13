"""LLMTool class for ReXia.AI"""

from typing import Any, List, Dict
from ...base import BaseWorker
from ...structure import RexiaAIResponse
from ...common import ContainerisedToolRunner

PREDEFINED_PROMPT = """
As an AI assistant for ReXia.AI, your task is to implement Python function(s) that will solve the given problem. Follow these guidelines:

Environment:
- Python 3.12
- Isolated container with only built-in libraries
- No external libraries, API keys, environment variables, or system-specific features

Key points:
- Use only Python's built-in libraries and functions
- Do not import or use any external packages
- Avoid any operations requiring API keys, network calls, or file operations
- Implement efficient, Pythonic code with appropriate built-ins
- Handle errors and edge cases
- Provide clear docstrings and type hints

Style guidelines:
- Use 4 spaces for indentation
- Maximum 100 characters per line
- Use snake_case for function and variable names
- Include concise docstrings and type hints

Implementation:
- Define the function(s) necessary to solve the given problem
- Include necessary import statements only from built-in modules
- Implement the required logic using only built-in Python features
- Create a main() function that solves the problem and returns the result

Output format:
- Provide code in the "answer" field as a list of strings
- Each string represents one line of code
- Preserve indentation with EXACTLY 4 spaces per level
- Include empty lines as empty strings
- The code will be joined and executed directly
- Ensure there is a main() function that returns the final result

Example output format:

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

Now, implement the solution for the following problem:
"""

class LLMTool(BaseWorker):
    """
    A worker for ReXia AI that generates Python tools based on given tasks.

    This class extends BaseWorker to provide specialized functionality for
    generating and executing Python code tools using a language model.

    Attributes:
        tool_runner (ContainerisedToolRunner): An instance of ContainerisedToolRunner
            used to execute the generated code in a secure environment.
    """

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
        max_attempts: int = 5,
    ):
        """
        Initialize an LLMTool instance.

        Args:
            model (Any): The language model to be used for generating code.
            verbose (bool, optional): If True, enables verbose output. Defaults to False.
            max_attempts (int, optional): Maximum number of attempts to generate
                working code. Defaults to 5.
        """
        super().__init__(model, verbose=verbose, max_attempts=max_attempts)
        self.tool_runner = ContainerisedToolRunner()

    def create_prompt(self, task: str, messages: List[str], memory: Any) -> str:
        """
        Create a prompt for the language model to generate a Python tool.

        This method constructs a prompt by combining a predefined prompt template
        with the specific task description.

        Args:
            task (str): The task description for which to create a tool.
            messages (List[str]): List of previous messages in the conversation.
            memory (Any): The memory object containing relevant context.

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
        prompt = super().create_prompt(PREDEFINED_PROMPT + task_prompt, task, messages, memory)
        return prompt

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
        """
        for attempt in range(self.max_attempts):
            try:
                agent_response = self._invoke_model(prompt)
                if not isinstance(agent_response, RexiaAIResponse):
                    raise ValueError(f"Expected RexiaAIResponse, got {type(agent_response)}")

                 # Join the list of code lines into a single string
                code = "\n".join(agent_response.answer) if isinstance(agent_response.answer, list) else agent_response.answer
                
                if self.verbose:
                    print(f"Attempt {attempt + 1}")
                    print("Code to execute:")
                    print(code)

                # Execute the generated code
                result = self.tool_runner.execute_code(code)

                if result.get("success"):
                    # If execution was successful, log the result
                    output = result.get("output", "No output")
                    print(f"Tool execution successful. Output: {output}")
                    return self._format_response(worker_name, agent_response, result)
                else:
                    # If execution failed, prepare error message for next attempt
                    error_message = f"Error: {result['error']}"
                    if self.verbose:
                        print(error_message)
                    prompt += f"\n\nThe previous code resulted in an error. Please fix and try again:\n{error_message}"
            except Exception as e:
                print(f"Error during attempt {attempt + 1}: {str(e)}")

        # If all attempts fail, return a failure response
        return self._format_response(
            worker_name,
            "Maximum attempts reached. Could not create a working tool.",
            {"success": False, "error": "Max attempts exceeded"}
        )

    def _format_response(
        self, worker_name: str, agent_response: Any, results: Dict
    ) -> str:
        """
        Format the final response including worker identification, raw agent response, and tool call results.

        This method creates a structured response containing the worker's name,
        the raw response from the agent, and the results of the tool execution.

        Args:
            worker_name (str): Identifier for the worker formatting the response.
            agent_response (Any): The raw response generated by the agent.
            results (Dict): Results of the tool calls made during the action.

        Returns:
            str: A formatted string containing the worker's response and tool call results.
        """
        formatted_response = {
            "worker_name": worker_name,
            "agent_response": str(agent_response),
            "tool_results": results
        }
        
        return str(formatted_response)