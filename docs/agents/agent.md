# ReXia.AI Agent Class

## Overview

The `Agent` class is a core component of the ReXia.AI framework. It is responsible for running workflows, reflecting on tasks, and interacting with language models to achieve desired outcomes. This documentation provides a detailed overview of the `Agent` class, its attributes, methods, and usage.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Class Attributes](#class-attributes)
- [Methods](#methods)
- [Examples](#examples)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use the `Agent` class, ensure you have the necessary dependencies installed. You can install them using pip:

```bash
pip install rexia-ai
```

## Usage

To create and use an `Agent` instance, follow the steps below:

```python
from rexia_ai.agent import Agent
from rexia_ai.memory import WorkingMemory
from rexia_ai.workflows import ReflectWorkflow

# Initialize the language model (llm) and task
llm = ...  # Your language model instance
task = "Your task description"

# Create an Agent instance
agent = Agent(llm=llm, task=task, workflow=ReflectWorkflow, memory=WorkingMemory(), verbose=True)

# Invoke the agent to perform the task
result = agent.invoke()
print(result)
```

## Class Attributes

- `workflow`: The workflow used by the agent.
- `task`: The task assigned to the agent.
- `llm`: The language model used by the agent.
- `verbose`: A flag for enabling verbose mode.
- `max_attempts`: The maximum number of attempts to get a valid response from the model.

## Methods

### `__init__(self, llm: Any, task: str, workflow: Optional[Type[BaseWorkflow]] = None, memory: BaseMemory = WorkingMemory(), verbose: bool = False, max_attempts: int = 3)`

Initializes an `Agent` instance.

**Parameters:**

- `llm`: The language model used by the agent.
- `task`: The task assigned to the agent.
- `workflow`: The class of the workflow to be used by the agent. Defaults to `ReflectWorkflow`.
- `memory`: The memory instance used by the agent. Defaults to `WorkingMemory`.
- `verbose`: A flag for enabling verbose mode. Defaults to `False`.
- `max_attempts`: The maximum number of attempts to get a valid response from the model. Defaults to `3`.

### `run_workflow(self) -> List[str]`

Runs the workflow and returns the messages.

**Returns:**

- `List[str]`: The messages from the workflow.

### `get_task_result(self, messages: List[str]) -> Optional[str]`

Extracts the task result from the messages.

**Parameters:**

- `messages`: The messages from which to extract the task result.

**Returns:**

- `Optional[str]`: The task result if it exists, `None` otherwise.

### `invoke(self, task: str = None) -> Optional[str]`

Invokes the agent to perform the task.

**Parameters:**

- `task`: The task to be performed by the agent. If not provided, the agent uses its assigned task.

**Returns:**

- `Optional[str]`: The accepted answer if it exists, `None` otherwise.

### `format_accepted_answer(self, answer: str) -> Optional[RexiaAIResponse]`

Formats the accepted answer by removing any single word before the JSON object.

**Parameters:**

- `answer`: The accepted answer to format.

**Returns:**

- `Optional[RexiaAIResponse]`: The formatted `RexiaAIResponse` if it exists and is valid, `None` otherwise.

## Examples

Here is an example of how to use the `Agent` class:

```python
from rexia_ai.agent import Agent
from rexia_ai.memory import WorkingMemory
from rexia_ai.workflows import ReflectWorkflow

# Initialize the language model (llm) and task
llm = ...  # Your language model instance
task = "Translate the following text to French."

# Create an Agent instance
agent = Agent(llm=llm, task=task, workflow=ReflectWorkflow, memory=WorkingMemory(), verbose=True)

# Invoke the agent to perform the task
result = agent.invoke()
print(result)
```

## Dependencies

- `rexia-ai`
- `re`
- `typing`

Ensure all dependencies are installed to avoid any issues.

## Contributing

We welcome contributions to improve the ReXia.AI framework. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

This README provides a comprehensive overview of the `Agent` class, including its usage, attributes, methods, and examples. Feel free to customize it further based on your specific needs and project structure.