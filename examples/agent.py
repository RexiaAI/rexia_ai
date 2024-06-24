"""Example agent in ReXia.AI."""

# Import necessary modules
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent

YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

# Create an instance of the RexiaAI LLM
llm = RexiaAIOpenAI(
    base_url="http://localhost:1234/v1",
    temperature=0,
    model="lm-studio"
)

# Create an instance of the RexiaAI Agent with the specified task and LLM
agent = Agent(llm=llm, task="What is the capital of France?", verbose=True)

# Generate the response from the agent
response = agent.invoke()

# Print the response
print("Response:", response)
