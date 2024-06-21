"""Example of how to use ReXia.AI's built in working memory. By default to max length of the memory is 10 messages."""

# Import necessary modules
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.tools import RexiaAIGoogleSearch

# Retrieve the Google API key and search engine ID from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Create an instance of the RexiaAIGoogleSearch tool
google_search = RexiaAIGoogleSearch(api_key=GOOGLE_API_KEY, engine_id=SEARCH_ENGINE_ID)

# Create a dictionary mapping the tool name to its instance
tools = {"google_search": google_search}

# Create an instance of the RexiaAI LLM
llm = RexiaAIOpenAI(
    base_url="http://localhost:1234/v1",
    model="llmware/bling-phi-3-gguf",
    api_key="lm-studio",
    temperature=0.0,
    tools=tools,
)

# Create an instance of the RexiaAI Agent with the specified task and LLM
agent = Agent(
    llm=llm,
    task="What is the capital of France?",
)

# Generate the response from the agent
agent.reflect()

agent.reflect(task="What is the last question you were asked?")

# Print the memory
print("Memory:", agent.workflow.memory.get_messages_as_string())
