# ReXia.AI Query Knowledge Base Tool

## Overview

The `RexiaAIQueryKnowledgeBase` class is a tool within the ReXia.AI framework that allows agents to query a knowledge base using large language models. This tool is designed to enable smaller local models to access information or assistance from larger, more capable models.

## Table of Contents

- [Class Attributes](#class-attributes)
- [Methods](#methods)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Class Attributes

- `llm`: An instance of the RexiaAIOpenAI class, configured with the specified model and temperature.

## Methods

### `__init__(self, base_url: str, api_key: str, model: str, temperature: float) -> None`

Initializes a RexiaAIQueryKnowledgeBase instance.

**Parameters:**

- `base_url`: The base URL for the large language model API.
- `api_key`: The API key for the large language model API.
- `model`: The model identifier for querying the knowledge base.
- `temperature`: The temperature to control the randomness of model responses.

### `query_knowledge_base(self, query: str) -> str`

Queries the knowledge base with the given query and returns the model's response.

**Parameters:**

- `query`: The task or query to be sent to the knowledge base.

**Returns:**

- The response from the knowledge base to the given query.

### `to_rexiaai_tool(self) -> list`

Returns the tool as a JSON object for ReXia.AI.

**Returns:**

- The tool as a JSON object.

### `to_rexiaai_function_call(self) -> dict`

Returns the tool as a dictionary object for ReXia.AI.

**Returns:**

- The tool as a dictionary object.

## Usage

Here's an example of how to use the `RexiaAIQueryKnowledgeBase` class:

```python
from rexia_ai.tools import RexiaAIQueryKnowledgeBase
from rexia_ai.agent import Agent
from rexia_ai.workflows import SimpleToolWorkflow
from rexia_ai.memory import WorkingMemory

# Initialize the RexiaAIQueryKnowledgeBase instance
knowledge_base_tool = RexiaAIQueryKnowledgeBase(
    base_url="https://api.example.com",
    api_key="your-api-key",
    model="gpt-3.5-turbo",
    temperature=0.7
)

# Create an Agent instance with SimpleToolWorkflow and the knowledge base tool
agent = Agent(
    llm=...,  # Your language model instance
    task="Query the knowledge base for information",
    workflow=SimpleToolWorkflow,
    memory=WorkingMemory(),
    verbose=True,
    tools={"query_knowledge_base": knowledge_base_tool}
)

# Run the agent
result = agent.invoke("What is the capital of France?")
print(result)
```

## Dependencies

- ReXia.AI components (`RexiaAIOpenAI`)

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
