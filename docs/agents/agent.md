# ReXia.AI Agent Class

## Overview

The `Agent` class is a core component of the ReXia.AI framework. It is responsible for running workflows, reflecting on tasks, and interacting with language models to achieve desired outcomes. This documentation provides a detailed overview of the `Agent` class, its attributes, methods, and usage, including the new task complexity routing feature.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Class Attributes](#class-attributes)
- [Methods](#methods)
- [Task Complexity Routing](#task-complexity-routing)
- [Examples](#examples)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use the `Agent` class, ensure you have the necessary dependencies installed. You can install them using pip:

```bash
pip install rexia_ai
```

## Usage

To create and use an `Agent` instance, follow the steps below:

```python
from rexia_ai.agent import Agent
from rexia_ai.memory import WorkingMemory
from rexia_ai.workflows import ReflectWorkflow
from rexia_ai.llms import RexiaAIOpenAI

# Initialize the language models
base_llm = RexiaAIOpenAI(...)
router_llm = RexiaAIOpenAI(...)
complex_llm = RexiaAIOpenAI(...)

# Create an Agent instance with routing
agent = Agent(
    llm=base_llm,
    task="Your task description",
    workflow=ReflectWorkflow,
    memory=WorkingMemory(),
    verbose=True,
    use_router=True,
    router_llm=router_llm,
    complex_llm=complex_llm,
    task_complexity_threshold=50
)

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
- `router`: The TaskComplexityRouter instance, if routing is enabled.
- `task_complexity`: The complexity score of the current task, if routing is enabled.

## Methods

### `__init__(self, llm: RexiaAIOpenAI, task: str, workflow: Optional[Type[BaseWorkflow]] = None, memory: BaseMemory = WorkingMemory(), verbose: bool = False, max_attempts: int = 3, use_router: bool = False, router_llm: Optional[RexiaAIOpenAI] = None, complex_llm: Optional[RexiaAIOpenAI] = None, task_complexity_threshold: int = 50)`

Initializes an `Agent` instance.

**Parameters:**

- `llm`: The base language model used by the agent.
- `task`: The task assigned to the agent.
- `workflow`: The class of the workflow to be used by the agent. Defaults to `ReflectWorkflow`.
- `memory`: The memory instance used by the agent. Defaults to `WorkingMemory`.
- `verbose`: A flag for enabling verbose mode. Defaults to `False`.
- `max_attempts`: The maximum number of attempts to get a valid response from the model. Defaults to `3`.
- `use_router`: Whether to use the task complexity router. Defaults to `False`.
- `router_llm`: The language model used for the router. Required if `use_router` is `True`.
- `complex_llm`: The language model used for complex tasks. Required if `use_router` is `True`.
- `task_complexity_threshold`: The threshold for determining when to use the complex model. Defaults to `50`.

### `run_workflow(self) -> List[str]`

Runs the workflow and returns the messages.

### `get_task_result(self, messages: List[str]) -> Optional[str]`

Extracts the task result from the messages.

### `invoke(self, task: str = None) -> Optional[str]`

Invokes the agent to perform the task. If a new task is provided, it updates the current task and recalculates the complexity if routing is enabled.

### `format_accepted_answer(self, answer: str) -> Optional[RexiaAIResponse]`

Formats the accepted answer by removing any single word before the JSON object.

## Task Complexity Routing

The `Agent` class now supports task complexity routing, which allows it to dynamically choose between a base language model and a more complex model based on the assessed complexity of the task.

### How it works

1. When `use_router` is set to `True`, a `TaskComplexityRouter` instance is created.
2. The router uses the `router_llm` to assess the complexity of the given task.
3. If the complexity score exceeds the `task_complexity_threshold`, the `complex_llm` is used for the task. Otherwise, the `base_llm` is used.
4. The complexity assessment is performed each time a new task is provided to the `invoke` method.

### Benefits

- Efficient resource allocation: Simple tasks use the faster, less resource-intensive base model.
- Improved performance on complex tasks: Difficult tasks are handled by the more capable complex model.
- Dynamic adaptation: The agent can switch between models as task complexity changes.

## Examples

Here's an example of how to use the `Agent` class with task complexity routing:

```python
from rexia_ai.agent import Agent
from rexia_ai.llms import RexiaAIOpenAI

# Initialize the language models
base_llm = RexiaAIOpenAI(base_url="http://localhost:1234/v1", model="yi-1.5", temperature=0)
router_llm = RexiaAIOpenAI(base_url="http://localhost:1234/v1", model="yi-1.5", temperature=0)
complex_llm = RexiaAIOpenAI(base_url="https://api.01.ai/v1", model="yi-large", temperature=0, api_key=YI_LARGE_API_KEY)

# Create an Agent instance with routing
agent = Agent(
    llm=base_llm,
    task="What is the capital of France?",
    verbose=True,
    use_router=True,
    router_llm=router_llm,
    complex_llm=complex_llm,
    task_complexity_threshold=50
)

# Invoke the agent with a simple task
response = agent.invoke()
print("Response:", response)

# Invoke the agent with a more complex task
complex_task = """Write a 500-word explanation of how photosynthesis works in plants, 
                  including the light-dependent and light-independent reactions. Describe the role of chlorophyll, 
                  the importance of water and carbon dioxide, and how the process produces glucose and oxygen. 
                  Then, discuss how this process impacts the global carbon cycle and its significance for life on Earth."""
response = agent.invoke(task=complex_task)
print("Response:", response)
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
