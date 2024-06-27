""" Simple tool using agent example. """

import os
from rexia_ai.agents import Agent
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.workflows import SimpleToolWorkflow
from rexia_ai.tools import RexiaAIQueryKnowledgeBase

YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")
YI_LARGE_BASE_URL = "https://api.01.ai/v1"

query_knowledge_base = RexiaAIQueryKnowledgeBase(api_key=YI_LARGE_API_KEY, base_url=YI_LARGE_BASE_URL, model="yi-large", temperature=0)

# Create a dictionary mapping the tool name to its instance
tools = {"query_knowledge_base": query_knowledge_base}

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
    task="Plan a long weekend in Paris for me, I want to know where to visit, where to stay, and where to eat.",
    workflow=SimpleToolWorkflow,
    verbose=True,
)

response = agent.invoke()

print("Response:", response)
    
