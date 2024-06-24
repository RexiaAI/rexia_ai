# ReXia.AI RexiaAILLMWare Class

## Overview

The `RexiaAILLMWare` class is a specialized language model implementation in the ReXia.AI framework. It provides compatibility with LLMware models, allowing for easy integration of various pre-trained models into the ReXia.AI ecosystem.

## Table of Contents

- [Class Attributes](#class-attributes)
- [Methods](#methods)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Class Attributes

- `tools`: A dictionary of tools available for the LLM.
- `model`: The model used for the LLM.

## Methods

### `__init__(self, model: str, temperature: float, tools: Optional[Dict[str, BaseTool]] = None, use_gpu: bool = False) -> None`

Initializes a RexiaAILLMWare instance.

**Parameters:**

- `model`: The model to use for the LLM.
- `temperature`: The temperature to use for text generation.
- `tools`: A dictionary of tools available for the LLM. Defaults to None.
- `use_gpu`: A flag to enable GPU usage. Defaults to False.

### `invoke(self, query: str, add_context: str = "") -> Optional[str]`

Perform inference using the language model.

**Parameters:**

- `query`: The query to perform inference on.
- `add_context`: Additional context to add to the query. Defaults to an empty string.

**Returns:**

- The response from the language model, or None if an error occurs.

## Usage

Here's an example of how to use the `RexiaAILLMWare` class:

```python
from rexia_ai.llm import RexiaAILLMWare
from rexia_ai.agent import Agent
from rexia_ai.workflows import SimpleToolWorkflow
from rexia_ai.memory import WorkingMemory

# Initialize the RexiaAILLMWare instance
llm = RexiaAILLMWare(
    model="llmware-model-name",
    temperature=0.7,
    use_gpu=True
)

# Define the task
task = "Summarize the following text."

# Create a memory instance
memory = WorkingMemory()

# Create an Agent instance with SimpleToolWorkflow and RexiaAILLMWare
agent = Agent(
    llm=llm,
    task=task,
    workflow=SimpleToolWorkflow,
    memory=memory,
    verbose=True
)

# Run the agent
result = agent.invoke()
print(result)
```

## Dependencies

- `typing`
- `pydantic`
- `llmware`
- ReXia.AI components (`BaseTool`)

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