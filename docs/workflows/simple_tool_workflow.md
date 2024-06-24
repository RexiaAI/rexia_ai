# ReXia.AI SimpleToolWorkflow Class

## Overview

The `SimpleToolWorkflow` class is a specialized workflow implementation in the ReXia.AI framework. It extends the `BaseWorkflow` class and implements a straightforward approach to task solving, focusing on tool usage and work execution. This workflow is designed to be used within an Agent instance.

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
- `tool`: The tool component of the workflow.
- `work`: The work component of the workflow.

## Methods

### `__init__(self, llm: Any, task: str, memory: BaseMemory, verbose: bool = False, max_attempts: int = 3) -> None`

Initializes a SimpleToolWorkflow instance.

**Parameters:**

- `llm`: The language model used by the workflow.
- `task`: The task assigned to the workflow.
- `memory`: The memory instance used by the workflow.
- `verbose`: A flag for enabling verbose mode. Defaults to `False`.
- `max_attempts`: The maximum number of attempts to get a valid response from the model. Defaults to `3`.

### `_run_task(self) -> None`

Internal method that executes the main workflow process.

### `run(self) -> None`

Public method to initiate the workflow execution.

## Usage

Here's an example of how to use the `SimpleToolWorkflow` class with an Agent:

```python
from rexia_ai.workflows import SimpleToolWorkflow
from rexia_ai.memory import WorkingMemory
from rexia_ai.agent import Agent

# Initialize your language model
llm = ...  # Your language model instance

# Define the task
task = "Perform a web search and summarize the results."

# Create a memory instance
memory = WorkingMemory()

# Create an Agent instance with SimpleToolWorkflow
agent = Agent(
    llm=llm,
    task=task,
    workflow=SimpleToolWorkflow,
    memory=memory,
    verbose=True
)

# Run the agent (which will use the SimpleToolWorkflow)
result = agent.invoke()
print(result)
```

## Components

The `SimpleToolWorkflow` utilizes two main components:

1. **Tool**: Handles the usage of any tools provided by the language model.
2. **Work**: Executes the main work based on the tool usage.

Each component is initialized with a specific worker (ToolWorker and Worker) that defines its behavior.

## Dependencies

- `typing`
- ReXia.AI components (`BaseWorkflow`, `BaseMemory`, `CollaborationChannel`, `TaskStatus`, `Component`)
- ReXia.AI workers (`Worker`, `ToolWorker`)
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
