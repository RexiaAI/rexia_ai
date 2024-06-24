# ReXia.AI RexiaAIOpenAI Class

## Overview

The `RexiaAIOpenAI` class is a specialized language model implementation in the ReXia.AI framework. It provides compatibility with OpenAI endpoints, allowing for easy integration of various OpenAI models into the ReXia.AI ecosystem.

## Table of Contents

- [Class Attributes](#class-attributes)
- [Methods](#methods)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Class Attributes

- `tools`: A dictionary of tools available for the LLM.

## Methods

### `__init__(self, base_url: str, model: str, temperature: float, tools: Optional[Dict[str, BaseTool]] = None, api_key: Optional[str] = None, max_tokens: int = 4096) -> None`

Initializes a RexiaAIOpenAI instance.

**Parameters:**

- `base_url`: The base URL for the OpenAI API.
- `model`: The model to use for the LLM.
- `temperature`: The temperature to use for text generation.
- `tools`: A dictionary of tools available for the LLM. Defaults to None.
- `api_key`: The API key for the OpenAI API. Defaults to None.
- `max_tokens`: The maximum number of tokens to generate. Defaults to 4096.

### `invoke(self, query: str) -> Optional[str]`

Perform inference using the language model.

**Parameters:**

- `query`: The query to perform inference on.

**Returns:**

- The response from the language model, or None if an error occurs.

## Usage

Here's an example of how to use the `RexiaAIOpenAI` class:

```python
from rexia_ai.llm import RexiaAIOpenAI
from rexia_ai.agent import Agent
from rexia_ai.workflows import SimpleToolWorkflow
from rexia_ai.memory import WorkingMemory

# Initialize the RexiaAIOpenAI instance
llm = RexiaAIOpenAI(
    base_url="https://api.openai.com/v1",
    model="text-davinci-003",
    temperature=0.7,
    api_key="your-openai-api-key"
)

# Define the task
task = "Summarize the following text."

# Create a memory instance
memory = WorkingMemory()

# Create an Agent instance with SimpleToolWorkflow and RexiaAIOpenAI
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
- `langchain_openai`
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
