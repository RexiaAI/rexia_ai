# ReXia.AI YouTube Video Analysis Tool

## Overview

The `RexiaAIYoutubeVideoAnalysis` class is a specialized tool in the ReXia.AI framework designed to analyze YouTube videos. It uses OpenAI's Whisper for audio transcription and a multimodal model to analyze video frames and transcripts, providing comprehensive insights based on user queries.

## Table of Contents

- [Class Attributes](#class-attributes)
- [Methods](#methods)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Class Attributes

- `openai_api_key`: OpenAI API key for accessing the models.
- `vision_model_base_url`: Base URL for the vision model.
- `vision_model`: Name of the vision model to use.
- `whisper_model`: Name of the Whisper model to use for transcription (default: "base").

## Methods

### `__init__(self, vision_model_base_url: str, vision_model: str, openai_api_key: str, whisper_model: str = "base") -> None`

Initializes a RexiaAIYoutubeVideoAnalysis instance.

### `analyse_video(self, query: str, video_url: str) -> str`

Analyzes the video and extracts insights based on the given query.

**Parameters:**

- `query`: The query or question about the video.
- `video_url`: The URL of the YouTube video to analyze.

**Returns:**

- The analysis and insights extracted from the video.

### `_process_video(self, video_url: str, seconds_per_frame: int = 2) -> Tuple[list, str]`

Extracts frames and audio from a video file.

### `_transcribe(self, audio_path: str) -> str`

Generates a transcription of the audio file.

### `to_rexiaai_tool(self) -> list`

Returns the tool as a JSON object for ReXia.AI.

### `to_rexiaai_function_call(self) -> dict`

Returns the tool as a dictionary object for ReXia.AI.

## Usage

Here's an example of how to use the `RexiaAIYoutubeVideoAnalysis` class:

```python
from rexia_ai.tools import RexiaAIYoutubeVideoAnalysis
from rexia_ai.agent import Agent
from rexia_ai.workflows import SimpleToolWorkflow
from rexia_ai.memory import WorkingMemory

# Initialize the RexiaAIYoutubeVideoAnalysis instance
video_analysis_tool = RexiaAIYoutubeVideoAnalysis(
    vision_model_base_url="https://api.openai.com/v1",
    vision_model="gpt-4-vision-preview",
    openai_api_key="your-openai-api-key"
)

# Create an Agent instance with SimpleToolWorkflow and the video analysis tool
agent = Agent(
    llm=...,  # Your language model instance
    task="Analyze the content of this YouTube video",
    workflow=SimpleToolWorkflow,
    memory=WorkingMemory(),
    verbose=True,
    tools={"analyse_video": video_analysis_tool}
)

# Run the agent
result = agent.invoke(
    "What is the main topic of this video?",
    video_url="https://www.youtube.com/watch?v=example"
)
print(result)
```

## Dependencies

- `uuid`
- `os`
- `base64`
- `typing`
- `pytube`
- `cv2`
- `moviepy`
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