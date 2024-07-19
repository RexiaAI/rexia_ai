""" Simple tool using agent example. """

import os
from rexia_ai.agents import Agent
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.workflows import SimpleToolWorkflow
from rexia_ai.tools import RexiaAIGoogleSearch

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

google_search = RexiaAIGoogleSearch(api_key=GOOGLE_API_KEY, engine_id=SEARCH_ENGINE_ID)

# Create a dictionary mapping the tool name to its instance
tools = {"google_search": google_search}

# Create an instance of the ReXiaAI LLM
llm = RexiaAIOpenAI(
    base_url="http://localhost:1234/v1",
    model="lm-studio",
    temperature=0,
    tools=tools,
)

# Create an instance of the ReXiaAI Agent with the specified task, LLM and workflow
agent = Agent(
    llm=llm,
    task="What is the capital of France?",
    workflow=SimpleToolWorkflow,
    verbose=True,
)

response = agent.invoke()

print("Response:", response)
    
