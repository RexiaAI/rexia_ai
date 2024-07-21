"""TDD Worker class for ReXia.AI."""

import inspect
from typing import Any, List, Dict
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from ...base import BaseWorker
from ...common import ContainerisedCodeTester
from ...structure import RexiaAIResponse

class CodeGenerationError(Exception):
    pass

class CodeExecutionError(Exception):
    pass

PREDEFINED_PROMPT = """
As a test-driven development agent for ReXia.AI, implement Python function(s) to pass the given unit test.

Environment:
- Python 3.12
- Isolated container with only built-in libraries
- No external libraries, environment variables, or system-specific features

Style guidelines:
- 4 spaces for indentation
- Max 100 characters per line
- snake_case for names
- Include type hints and concise docstrings

Implementation:
- Include all necessary import statements at the beginning of your code
- Implement only required function(s)
- Use efficient, Pythonic code with appropriate built-ins
- Handle errors and edge cases
- No sensitive info, network calls, or file operations

Key points:
- Match function name(s) in the test
- Ensure correct inputs and outputs
- Account for edge cases

Output format:
- Provide code in "answer" field as a list of strings
- Each string = one line of code
- Preserve indentation with EXACTLY 4 spaces per level
- Include empty lines as empty strings
- Code will be joined and executed directly

Example output format:
{
    "question": "Implement a sum_numbers function to pass the given test.",
    "plan": [
        "Import necessary modules",
        "Define the sum_numbers function with appropriate type hints",
        "Implement logic to handle different input types (int, float, str, list)",
        "Use recursion to handle nested lists",
        "Implement error handling for invalid inputs"
    ],
    "answer": [
        "from typing import Union, List",
        "",
        "def sum_numbers(*args: Union[int, float, str, List[Union[int, float]]]) -> Union[int, float]:",
        "    total: Union[int, float] = 0",
        "    for arg in args:",
        "        if isinstance(arg, list):",
        "            total += sum_numbers(*arg)",
        "        elif isinstance(arg, (int, float)):",
        "            total += arg",
        "        elif isinstance(arg, str):",
        "            try:",
        "                total += float(arg)",
        "            except ValueError:",
        "                raise ValueError(\"Invalid number string\")",
        "        else:",
        "            raise TypeError(\"Unsupported argument type\")",
        "    return total"
    ],
    "confidence_score": 95.0,
    "chain_of_reasoning": [
        "Import necessary modules (typing for type hints)",
        "Define function signature with appropriate type hints",
        "Initialize total variable to store the sum",
        "Iterate through all arguments",
        "Handle list inputs recursively",
        "Add numeric inputs directly to total",
        "Convert string inputs to float and add to total",
        "Raise appropriate errors for invalid inputs",
        "Return the final total"
    ],
    "tool_calls": []
}
"""

class TDDWorker(BaseWorker):
    """
    A Test-Driven Development worker for ReXia AI.
    This worker is responsible for generating Python code that passes
    the provided unit tests.
    """

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
    ):
        """
        Initialize a TDDWorker instance.

        Args:
            model: The model used by the worker.
            verbose: A flag used for enabling verbose mode. Defaults to False.
        """
        super().__init__(model, verbose=verbose)
        self.test_class = None
        self.test_globals = {}

    def set_test_class(self, test_class: type):
        """Set the test class to be used for TDD."""
        self.test_class = test_class

    def create_prompt(self, task: str, messages: List[str], memory: Any) -> str:
        """
        Create a prompt for the model.

        Args:
            task: The task description.
            messages: List of previous messages.
            memory: The memory object.

        Returns:
            A string containing the prompt for the model.

        Raises:
            ValueError: If the test class has not been set.
        """
        if self.test_class is None:
            raise ValueError(
                "Test class has not been set. Use set_test_class() before creating a prompt."
            )

        test_code = inspect.getsource(self.test_class)
        task_prompt = f"""
        Task overview: {task}

        Write Python code that will make the following test pass:

        {test_code}

        Implement the necessary function(s) to make all assertions in the test pass.
        Only provide the implementation, not the test class itself.
        """
        prompt = super().create_prompt(PREDEFINED_PROMPT, task_prompt, messages, memory)
        return prompt

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type(CodeGenerationError),
        reraise=True
    )
    def action(self, prompt: str, worker_name: str) -> str:
        """
        Execute the action of generating and testing code based on the given prompt.

        This method attempts to generate code using an AI model, execute it in a containerized
        environment, and run tests against it. It will make multiple attempts if the initial
        code generation or tests fail.

        Args:
            prompt (str): The initial prompt for code generation.
            worker_name (str): The name of the worker executing this action.

        Returns:
            str: A string containing the worker name and the result of the action.
                If successful, it includes the generated code. If unsuccessful after
                maximum attempts, it returns a failure message.

        Raises:
            RetryError: If all retry attempts fail.
        """
        try:
            agent_response = self._invoke_model(prompt)
            if not isinstance(agent_response, RexiaAIResponse):
                raise ValueError(f"Expected RexiaAIResponse, got {type(agent_response)}")

            if self.verbose:
                print(f"Agent response: {agent_response}")
                print(f"Code generated: {agent_response.answer}")

            code = agent_response.answer

            if self.verbose:
                print("Code to test:")
                print(code)

            executor = ContainerisedCodeTester()
            result = executor.execute_code(code, self.test_class)

            if result.get("all_passed"):
                return f"{worker_name}: {agent_response}"
            else:
                error_message = self._format_error_message(result)
                if self.verbose:
                    print(f"Attempt failed, retrying...")
                    print(error_message)
                prompt = self._update_prompt_with_error(prompt, agent_response, error_message)
                raise CodeGenerationError(error_message)

        except Exception as e:
            print(f"Error during attempt: {str(e)}")
            raise CodeGenerationError(str(e))

    def _update_prompt_with_error(self, prompt: str, agent_response: RexiaAIResponse, error_message: str) -> str:
        return f"""\nThe Python code within the answer field of this JSON object returned an error.
        JSON Object: {agent_response}\n\n 
        Error: {error_message}\n\n
        Please return the full previous JSON object with the answer updated to fix this error.
        """

    def _format_error_message(self, result: Dict[str, Any]) -> str:
        """
        Format the error message from the test results.

        Args:
            result: The test result dictionary.

        Returns:
            A formatted error message string.
        """
        error_message = "Test failures or errors:\n"
        for failure in result.get("failed", []):
            error_message += f"- Failed: {failure['name']}: {failure['error']}\n"
        for error in result.get("errors", []):
            error_message += f"- Error: {error['type']}: {error['message']}\n"
        if "error" in result:
            error_message += f"Error: {result['error']}\n"
        return error_message
