"""Example agent in ReXia.AI."""

# Import necessary modules
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent

# Create an instance of the RexiaAI LLM
llm = RexiaAIOpenAI(
    base_url="http://localhost:11434/v1",
    model="llama3.1",
    temperature=0
)

# Create an instance of the RexiaAI Agent with the specified task and LLM
agent = Agent(llm=llm, task="What is the capital of France?", verbose=True)

# Generate the response from the agent
response = agent.invoke()

# Print the response
print("Response:", response)
