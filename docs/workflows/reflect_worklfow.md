# ReXia.AI ReflectWorkflow Class

## Overview

The `ReflectWorkflow` class is a specialized workflow implementation in the ReXia.AI framework. It extends the `BaseWorkflow` class and implements a reflective approach to task solving, utilizing various components such as planning, tool usage, work execution, and finalization. This workflow is designed to be used within an Agent instance.

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
- `plan`: The plan component of the workflow.
- `tool`: The tool component of the workflow.
- `work`: The work component of the workflow.
- `finalise`: The finalise component of the workflow.

## Methods

### `__init__(self, llm: Any, task: str, memory: BaseMemory, verbose: bool = False, max_attempts: int = 3) -> None`

Initializes a ReflectWorkflow instance.

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

Here's an example of how to use the `ReflectWorkflow` class with an Agent:

```python
from rexia_ai.workflows import ReflectWorkflow
from rexia_ai.memory import WorkingMemory
from rexia_ai.agent import Agent

# Initialize your language model
llm = ...  # Your language model instance

# Define the task
task = "Analyze the given text and provide a summary."

# Create a memory instance
memory = WorkingMemory()

# Create an Agent instance with ReflectWorkflow
agent = Agent(
    llm=llm,
    task=task,
    workflow=ReflectWorkflow,
    memory=memory,
    verbose=True
)

# Run the agent (which will use the ReflectWorkflow)
result = agent.invoke()
print(result)
```

## Components

The `ReflectWorkflow` utilizes several components:

1. **Plan**: Responsible for creating a plan to accomplish the task.
2. **Tool**: Handles the usage of any tools provided by the language model.
3. **Work**: Executes the main work based on the plan and tool usage.
4. **Finalise**: Wraps up the task and provides the final output.

Each component is initialized with a specific worker (PlanWorker, ToolWorker, Worker, FinaliseWorker) that defines its behavior.

## Dependencies

- `typing`
- ReXia.AI components (`BaseWorkflow`, `BaseMemory`, `CollaborationChannel`, `TaskStatus`, `Component`)
- ReXia.AI workers (`PlanWorker`, `FinaliseWorker`, `Worker`, `ToolWorker`)
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
