""" Simple tool using agent example. """

from rexia_ai.agents import Agent
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.workflows import CollaborationWorkflow

# Create an instance of the ReXiaAI LLM
llm = RexiaAIOpenAI(
    base_url="http://localhost:1234/v1",
    model="lm-studio",
    temperature=0,
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
    
