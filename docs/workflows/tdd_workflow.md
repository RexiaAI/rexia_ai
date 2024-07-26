# ReXia.AI TDDWorkflow Class

## Overview

The `TDDWorkflow` class is a specialized workflow implementation in the ReXia.AI framework. It extends the `BaseWorkflow` class and implements a Test-Driven Development (TDD) approach to task solving, focusing on generating code that passes predefined tests. This workflow is designed to be used within an Agent instance and leverages a TDDWorker and ContainerisedCodeTester to execute the TDD process securely.

## Table of Contents

- [Class Attributes](#class-attributes)
- [Methods](#methods)
- [Usage](#usage)
- [Components](#components)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Class Attributes

- `llm`: The language model used by the workflow.
- `task`: The task that the workflow is designed to perform.
- `verbose`: A flag used for enabling verbose mode.
- `channel`: The collaboration channel for the workflow.
- `max_attempts`: The maximum number of attempts for code generation.
- `tdd`: The TDD component of the workflow.
- `test_class`: The class containing the test cases for the TDD process.

## Methods

### `__init__(self, llm: Any, task: str, verbose: bool = False, max_attempts: int = 5) -> None`

Initializes a TDDWorkflow instance.

**Parameters:**

- `llm`: The language model used by the workflow.
- `task`: The task assigned to the workflow.
- `verbose`: A flag for enabling verbose mode. Defaults to `False`.
- `max_attempts`: The maximum number of attempts for code generation. Defaults to `5`.

### `_run_task(self) -> None`

Internal method that executes the main TDD workflow process.

### `set_test_class(self, test_class: type) -> None`

Sets the test class to be used in the TDD process.

**Parameters:**

- `test_class`: The class containing the test cases for the TDD process.

### `run(self) -> str`

Public method to initiate the workflow execution.

## Usage

Here's an example of how to use the `TDDWorkflow` class with an Agent in ReXia.AI:

```python
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.workflows import TDDWorkflow

# Set up the language model
YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")
llm = RexiaAIOpenAI(
    base_url="http://localhost:1234/v1",
    model="yi-large",
    temperature=0
)

# Define the test class
class TestLLMCode:
    @classmethod
    def setUpClass(cls):
        import math
        from typing import Union, List
        cls.math = math
        cls.Union = Union
        cls.List = List
    
    @classmethod
    def test_sum_function(cls, func):
        assert func(5, 7) == 12, "5 + 7 should equal 12"
        assert func(-3, 3) == 0, "-3 + 3 should equal 0"
        assert func(0, 0) == 0, "0 + 0 should equal 0"
        assert func(1.5, 2.5) == 4.0, "1.5 + 2.5 should equal 4.0"
        assert func(-1.5, -2.5) == -4.0, "-1.5 + -2.5 should equal -4.0"

    @classmethod
    def test_sum_with_strings(cls, func):
        assert func("2", "3") == 5, "Sum of '2' and '3' as strings should be 5"
        assert func("-1", "1") == 0, "Sum of '-1' and '1' as strings should be 0"

    @classmethod
    def test_sum_type_hints(cls, func):
        import inspect
        signature = inspect.signature(func)
        assert signature.return_annotation == cls.Union[int, float], "Return type hint should be Union[int, float]"
        for param in signature.parameters.values():
            assert param.annotation == cls.Union[int, float, str, cls.List[cls.Union[int, float]]], \
                "Parameter type hints should be Union[int, float, str, List[Union[int, float]]]"

# Create an Agent instance with TDDWorkflow
agent = Agent(
    llm=llm,
    task="Create a sum_numbers function to pass the test.",
    verbose=True,
    workflow=TDDWorkflow
)

# Set the test class for the workflow
agent.workflow.set_test_class(TestLLMCode)

# Run the agent (which will use the TDDWorkflow)
response = agent.invoke()

# Print the response
print("Response:", response)
```

## Components

The `TDDWorkflow` utilizes two main components:

1. **TDDWorker**: Handles the Test-Driven Development process, including running tests and generating code.
2. **ContainerisedCodeTester**: Executes the generated code in an isolated Docker container.

### TDDWorker

The TDDWorker class is responsible for generating Python code that passes the provided unit tests. Key features include:

- Initialization with a language model, verbosity flag, and maximum number of attempts
- Setting a test class using `set_test_class()`
- Creating prompts for the language model using `create_prompt()`
- Executing the TDD process using the `action()` method

The `action()` method:

1. Generates code using the AI model
2. Executes the code in a containerized environment
3. Runs tests against the generated code
4. Makes multiple attempts (up to `max_attempts`) if the initial code generation or tests fail
5. Formats and returns error messages if tests fail

### ContainerisedCodeTester

The ContainerisedCodeTester class is responsible for executing the generated Python code in isolated Docker containers. Key features include:

- Initialization with a specified Docker image (default: "python:3.12-slim") and execution timeout
- Execution of code and associated tests in a controlled Docker environment
- Writing code and test files to a temporary directory
- Running the Docker container with the provided code and tests
- Parsing and returning the execution results

Key methods:

- `execute_code(code, test_class)`: Executes the provided code and test class in a Docker container
- `_write_files(tmpdir, code, test_class)`: Writes the code and test files to a temporary directory
- `_run_container(tmpdir)`: Runs the Docker container with the provided code and tests
- `_generate_main_test_logic(class_name, func_name)`: Generates the main test execution logic

The ContainerisedCodeTester ensures that the generated code runs in a secure, isolated environment with:

- Limited memory (128MB)
- Limited CPU quota
- No network access
- Read-only access to the code and test files

## Dependencies

- `typing`
- `docker`
- `tempfile`
- `ast`
- `os`
- `inspect`
- `json`
- `traceback`
- `textwrap`
- ReXia.AI components (`BaseWorkflow`, `BaseMemory`, `CollaborationChannel`, `TaskStatus`, `Component`)
- ReXia.AI workers (`TDDWorker`)
- ReXia.AI Agent class

Ensure all dependencies are installed and properly imported.

## Contributing

We welcome contributions to improve the ReXia.AI framework. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](../LICENSE) file for details.
