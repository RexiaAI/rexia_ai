"""Example agent in ReXia.AI using CodeToolWorkflow for a complex mathematical task."""

import os
from rexia_ai.agents import Agent
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.workflows import CodeToolWorkflow

YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

# Create an instance of the ReXiaAI LLM
llm = RexiaAIOpenAI(
    base_url="https://api.01.ai/v1",
    model="yi-large",
    temperature=0,
    api_key=YI_LARGE_API_KEY,
)

# Define a complex mathematical task
task = "Calculate the first 100 prime numbers and then find the sum of their digits."

# Create an instance of the ReXiaAI Agent with the specified task, LLM and workflow
agent = Agent(
    llm=llm,
    task=task,
    workflow=CodeToolWorkflow,
    verbose=True,
)

# Generate the response from the agent
response = agent.invoke()

print("Response:", response)