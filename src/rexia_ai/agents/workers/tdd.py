"""TDD Worker class for ReXia.AI."""

import inspect
from typing import Any, List, Dict
from ...base import BaseWorker
from ...common import ContainerisedCodeTester
from ...structure import RexiaAIResponse

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
        max_attempts: int = 5,
    ):
        """
        Initialize a TDDWorker instance.

        Args:
            model: The model used by the worker.
            verbose: A flag used for enabling verbose mode. Defaults to False.
            max_attempts: Maximum number of attempts to generate passing code. Defaults to 5.
        """
        super().__init__(model, verbose=verbose, max_attempts=max_attempts)
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
            ValueError: If the AI model response is not of the expected type.

        Note:
            - This method uses a ContainerizedCodeExecutor to run the generated code securely.
            - It will make up to self.max_attempts to generate passing code.
            - If verbose mode is enabled, it will print detailed information about each attempt.
        """
        for attempt in range(self.max_attempts):
            try:
                agent_response = self._invoke_model(prompt)
                if not isinstance(agent_response, RexiaAIResponse):
                    raise ValueError(
                        f"Expected RexiaAIResponse, got {type(agent_response)}"
                    )
                print(f"Agent response for attempt {attempt + 1}: {agent_response}")
                print(f"Code generated for attempt {attempt + 1}: {agent_response.answer}")

                code = agent_response.answer

                if self.verbose:
                    print(f"Attempt {attempt + 1}")
                    print("Code to test: ")
                    print(code)
                    
                # Execute the code in a container
                executor = ContainerisedCodeTester()
                result = executor.execute_code(code, self.test_class)

                if result.get("all_passed"):
                    return f"{worker_name}: {agent_response}"
                else:
                    print(f"Attempt {attempt + 1} failed, retrying...")
                    error_message = "Test failures or errors:\n"
                    for failure in result.get("failed", []):
                        error_message += (
                            f"- Failed: {failure['name']}: {failure['error']}\n"
                        )
                    for error in result.get("errors", []):
                        error_message += (
                            f"- Error: {error['type']}: {error['message']}\n"
                        )
                    if "error" in result:
                        error_message += f"Error: {result['error']}\n"

                    if self.verbose:
                        print(error_message)
                    prompt = f"""\nThe Python code within the answer field of this JSON object returned an error.
                        JSON Object: {agent_response}\n\n 
                        Error: {error_message}\n\n
                        
                        Please return the full previous JSON object with the answer updated to fix this error.
                        """
            except Exception as e:
                print(f"Error during attempt {attempt + 1}: {str(e)}")

        return (
            f"{worker_name}: Maximum attempts reached. Could not generate passing code."
        )

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
