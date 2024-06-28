# ReXia.AI

ReXia.AI is an advanced AI framework designed to integrate various language models, tools, and workflows for complex task solving and analysis. It provides a flexible and extensible platform for building AI-powered applications and agents.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Tools](#tools)
- [License](#license)
- [Contact](#contact)

## Update v0.1.6

- Added team_worker
- Added collaboration_workflow
- Added collaboration workflow example
- Added collaboration workflow documentation

## Features

- Support for multiple language models
- Extensible workflow system
- Built-in memory management
- Integration with various external tools and APIs
- Customizable agents for specific tasks

## Installation

To install ReXia.AI, you can use pip:

```bash
pip install rexia-ai
```

Additionally, you need to install either PyTorch or TensorFlow, depending on your preference:

For PyTorch:

```bash
pip install torch
```

For TensorFlow:

```bash
pip install tensorflow
```

## Quick Start

Here's a simple example to get you started with ReXia.AI:

```python
from rexia_ai.agent import Agent
from rexia_ai.workflows import SimpleToolWorkflow
from rexia_ai.memory import WorkingMemory
from rexia_ai.llm import RexiaAIOpenAI

# Initialize the language model
llm = RexiaAIOpenAI(
    base_url="https://api.openai.com/v1",
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key="your-openai-api-key"
)

# Create an Agent instance
agent = Agent(
    llm=llm,
    task="Summarize the latest news on AI advancements",
    workflow=SimpleToolWorkflow,
    memory=WorkingMemory(),
    verbose=True
)

# Run the agent
result = agent.invoke()
print(result)
```

## Documentation

Detailed documentation for each component can be found in the `docs` folder:

- [Agent](docs/agents/agent.md)
- [Workflows](docs/workflows)
- [Language Models](docs/llms)
- [Memory](docs/memory)
- [Tools](docs/tools)

## Tools

ReXia.AI comes with several built-in tools:

- [YouTube Video Analysis](docs/tools/youtube_video_analysis.md)
- [Google Search](docs/tools/google_search.md)
- [Image Analysis](docs/tools/image_analysis.md)
- [Alpha Vantage Financial Data](docs/tools/alpha_vantage.md)

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions, issues, or suggestions, please open an issue on our [GitHub repository](https://github.com/yourusername/rexia-ai/issues).
