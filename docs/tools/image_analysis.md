# ReXia.AI Image Analysis Tool

## Overview

The `RexiaAIImageAnalysis` class is a specialized tool in the ReXia.AI framework designed to analyze images. It works with any vision or multimodal model and has been tested on GPT-4o and llava phi 3. This tool allows text-based models to call a vision model to analyze images.

## Table of Contents

- [Class Attributes](#class-attributes)
- [Methods](#methods)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Class Attributes

- `api_key`: The API key for OpenAI.
- `vision_model_base_url`: The base URL for the vision model.
- `vision_model`: The name of the vision model.

## Methods

### `__init__(self, vision_model_base_url: str, vision_model: str, api_key: str) -> None`

Initializes a RexiaAIImageAnalysis instance.

**Parameters:**

- `vision_model_base_url`: The base URL for the vision model.
- `vision_model`: The name of the vision model.
- `api_key`: The API key for OpenAI.

### `analyse(self, query: str, image_path: str) -> str`

Processes an image and gets a response.

**Parameters:**

- `query`: The query to analyze.
- `image_path`: The path to the image file.

**Returns:**

- The analysis result.

### `_get_image_data(self, image_path: str) -> bytes`

Gets image data from a URL or a local path.

**Parameters:**

- `image_path`: The path to the image file.

**Returns:**

- The image data.

### `to_rexiaai_tool(self) -> list`

Returns the tool as a JSON object for ReXia.AI.

**Returns:**

- The tool as a JSON object.

### `to_rexiaai_function_call(self) -> dict`

Returns the tool as a dictionary object for ReXia.AI.

**Returns:**

- The tool as a dictionary object.

## Usage

Here's an example of how to use the `RexiaAIImageAnalysis` class:

```python
from rexia_ai.tools import RexiaAIImageAnalysis
from rexia_ai.agent import Agent
from rexia_ai.workflows import SimpleToolWorkflow
from rexia_ai.memory import WorkingMemory

# Initialize the RexiaAIImageAnalysis instance
image_analysis_tool = RexiaAIImageAnalysis(
    vision_model_base_url="https://api.openai.com/v1",
    vision_model="gpt-4-vision-preview",
    api_key="your-openai-api-key"
)

# Create an Agent instance with SimpleToolWorkflow and the image analysis tool
agent = Agent(
    llm=...,  # Your language model instance
    task="Analyze the content of this image",
    workflow=SimpleToolWorkflow,
    memory=WorkingMemory(),
    verbose=True,
    tools={"image_analysis": image_analysis_tool}
)

# Run the agent
result = agent.invoke(
    "What is the main topic of this image?",
    image_path="https://example.com/image.jpg"
)
print(result)
```

## Dependencies

- `base64`
- `requests`
- `openai`
- ReXia.AI components (`BaseTool`, `LLMOutput`)

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