# ReXia.AI WorkingMemory Class

## Overview

The `WorkingMemory` class is a component of the ReXia.AI framework that implements a working memory object. This memory persists between runs of an Agent instance, allowing for the retention and management of messages or information across multiple interactions.

## Table of Contents

- [Class Attributes](#class-attributes)
- [Methods](#methods)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Class Attributes

- `max_length`: The maximum number of messages to retain in memory.
- `messages`: A list of strings representing the stored messages.

## Methods

### `__init__(self, max_length: int = 10) -> None`

Initializes a WorkingMemory instance.

**Parameters:**

- `max_length`: The maximum number of messages to retain. Defaults to 10.

### `add_message(self, message: str) -> None`

Adds a message to the working memory.

**Parameters:**

- `message`: The message to add to the memory.

### `get_messages(self) -> List[str]`

Retrieves all messages from the working memory.

**Returns:**

- A list of all stored messages.

### `get_messages_as_string(self) -> str`

Retrieves all messages from the working memory as a single string.

**Returns:**

- A string containing all stored messages concatenated with spaces.

### `clear_messages(self) -> None`

Clears all messages from the working memory.

### `truncate_messages(self, max_length: int) -> None`

Truncates the working memory to the specified length.

**Parameters:**

- `max_length`: The maximum number of messages to retain.

## Usage

Here's an example of how to use the `WorkingMemory` class:

```python
from rexia_ai.memory import WorkingMemory
from rexia_ai.agent import Agent
from rexia_ai.workflows import SimpleToolWorkflow

# Initialize the WorkingMemory instance
memory = WorkingMemory(max_length=5)

# Create an Agent instance with the WorkingMemory
agent = Agent(
    llm=...,  # Your language model instance
    task="Perform a series of related tasks",
    workflow=SimpleToolWorkflow,
    memory=memory,
    verbose=True
)

# Run the agent multiple times
for i in range(3):
    result = agent.invoke(f"Task {i+1}")
    print(result)

# Check the contents of the memory
print(memory.get_messages_as_string())
```

## Dependencies

- `typing`
- ReXia.AI components (`BaseMemory`)

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
