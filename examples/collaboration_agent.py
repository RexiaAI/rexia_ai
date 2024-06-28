""" Simple tool using agent example. """

import os
from rexia_ai.agents import Agent
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.workflows import CollaborationWorkflow

YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

# Create an instance of the ReXiaAI LLM
llm = RexiaAIOpenAI(
    base_url="https://api.01.ai/v1",
    model="yi-large",
    temperature=0,
    api_key=YI_LARGE_API_KEY,
)

# Create an instance of the ReXiaAI Agent with the specified task, LLM and workflow
agent = Agent(
    llm=llm,
    task="I have £10,000 to invest in the stockmarket, I want to know the best strategy to make the most of my money.",
    workflow=CollaborationWorkflow,
    verbose=True,
)

response = agent.invoke()

print("Response:", response)
    
