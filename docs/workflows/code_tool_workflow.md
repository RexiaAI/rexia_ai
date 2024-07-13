# ReXia.AI CodeToolWorkflow Class

## Overview

The `CodeToolWorkflow` class is a specialized workflow implementation in the ReXia.AI framework. It extends the `BaseWorkflow` class and implements a process for generating and executing custom code tools to solve complex tasks. This workflow is designed to be used within an Agent instance and leverages a large language model (LLM) to dynamically create Python functions that can assist in completing the given task.

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
- `memory`: The memory component of the workflow.
- `channel`: The collaboration channel for the workflow.
- `max_attempts`: The maximum number of attempts for code generation.

## Methods

### `__init__(self, llm: Any, task: str, memory: BaseMemory, verbose: bool = False, max_attempts: int = 3) -> None`

Initializes a CodeToolWorkflow instance.

**Parameters:**

- `llm`: The language model used by the workflow.
- `task`: The task assigned to the workflow.
- `memory`: The memory instance used by the workflow.
- `verbose`: A flag for enabling verbose mode. Defaults to `False`.
- `max_attempts`: The maximum number of attempts for code generation. Defaults to `3`.

### `_run_task(self) -> None`

Internal method that executes the main CodeToolWorkflow process.

### `run(self) -> str`

Public method to initiate the workflow execution.

## Usage

Here's an example of how to use the `CodeToolWorkflow` class with an Agent in ReXia.AI:

```python
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.workflows import CodeToolWorkflow
from rexia_ai.memory import SimpleMemory

# Set up the language model
YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")
llm = RexiaAIOpenAI(
    base_url="https://api.01.ai/v1",
    model="yi-large",
    temperature=0,
    api_key=YI_LARGE_API_KEY,
)

# Define the task
task = "Calculate the sum of squares for the first 100 prime numbers."

# Create an Agent instance with CodeToolWorkflow
agent = Agent(
    llm=llm,
    task=task,
    workflow=CodeToolWorkflow,
    verbose=True
)

# Run the agent (which will use the CodeToolWorkflow)
response = agent.invoke()

# Print the response
print("Task:", task)
print("Response:", response)
```

## Components

The `CodeToolWorkflow` primarily utilizes the following components:

1. **Large Language Model (LLM)**: Generates Python code based on the given task.
2. **ContainerisedCodeTester**: Executes the generated code in an isolated Docker container.

### Large Language Model (LLM)

The LLM is responsible for generating Python code that can solve the given task. Key features include:

- Receiving a task description and generating appropriate Python functions
- Handling complex tasks by breaking them down into manageable steps
- Iteratively improving the generated code based on execution results

### ContainerisedCodeTester

The ContainerisedCodeTester class is responsible for executing the generated Python code in isolated Docker containers. Key features include:

- Initialization with a specified Docker image (default: "python:3.12-slim") and execution timeout
- Execution of code in a controlled Docker environment
- Writing code to a temporary directory
- Running the Docker container with the provided code
- Parsing and returning the execution results

Key methods:

- `execute_code(code)`: Executes the provided code in a Docker container
- `_write_files(tmpdir, code)`: Writes the code files to a temporary directory
- `_run_container(tmpdir)`: Runs the Docker container with the provided code
- `_parse_output(output)`: Parses the output from the Docker container

The ContainerisedCodeTester ensures that the generated code runs in a secure, isolated environment with:

- Limited memory (128MB)
- Limited CPU quota
- No network access
- Read-only access to the code files

## Dependencies

- `typing`
- `docker`
- `tempfile`
- `os`
- `json`
- ReXia.AI components (`BaseWorkflow`, `BaseMemory`, `CollaborationChannel`, `TaskStatus`, `Component`)
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
