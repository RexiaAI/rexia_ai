# ReXia.AI Google Search Tool

## Overview

The `RexiaAIGoogleSearch` class is an extension of the Google Search Tool from `langchain_community`, adapted to work more consistently with open-source models within the ReXia.AI framework. This tool allows agents to perform Google searches and retrieve results.

## Table of Contents

- [Class Attributes](#class-attributes)
- [Methods](#methods)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Class Attributes

- `api_key`: The API key for Google Search.
- `engine_id`: The engine ID for Google Search.
- `google_search_api`: An instance of GoogleSearchAPIWrapper from langchain_google_community.

## Methods

### `__init__(self, api_key: str, engine_id: str) -> None`

Initializes a RexiaAIGoogleSearch instance.

**Parameters:**

- `api_key`: The API key for Google Search.
- `engine_id`: The engine ID for Google Search.

### `google_search(self, query: str) -> str`

Runs a query through Google Search and parses the result.

**Parameters:**

- `query`: The search query to execute.

**Returns:**

- The search result as a string.

### `to_rexiaai_tool(self) -> list`

Returns the tool as a JSON object for ReXia.AI.

**Returns:**

- The tool as a JSON object.

### `to_rexiaai_function_call(self) -> dict`

Returns the tool as a dictionary object for ReXia.AI.

**Returns:**

- The tool as a dictionary object.

## Usage

Here's an example of how to use the `RexiaAIGoogleSearch` class:

```python
from rexia_ai.tools import RexiaAIGoogleSearch
from rexia_ai.agent import Agent
from rexia_ai.workflows import SimpleToolWorkflow
from rexia_ai.memory import WorkingMemory

# Initialize the RexiaAIGoogleSearch instance
google_search_tool = RexiaAIGoogleSearch(
    api_key="your-google-api-key",
    engine_id="your-google-engine-id"
)

# Create an Agent instance with SimpleToolWorkflow and the Google search tool
agent = Agent(
    llm=...,  # Your language model instance
    task="Search for information on a topic",
    workflow=SimpleToolWorkflow,
    memory=WorkingMemory(),
    verbose=True,
    tools={"google_search": google_search_tool}
)

# Run the agent
result = agent.invoke("What is the capital of France?")
print(result)
```

## Dependencies

- `langchain_google_community`
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

## Acknowledgments

Credit to the original authors of the `langchain_community` Google Search Tool, who did most of the work. This class extends their implementation to work more consistently with open-source models within ReXia.AI.
