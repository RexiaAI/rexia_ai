"""Example agent in ReXia.AI using CodeToolWorkflow for a complex mathematical task."""

from rexia_ai.agents import Agent
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.workflows import CodeToolWorkflow

# Create an instance of the ReXiaAI LLM
llm = RexiaAIOpenAI(
    base_url="http://localhost:1234/v1",
    model="lm-studio",
    temperature=0,
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