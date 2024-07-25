"""Example agent in ReXia.AI."""

# Import necessary modules
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.agencies import Agency, AgentInfo
from rexia_ai.workflows import SimpleToolWorkflow, CodeToolWorkflow
from rexia_ai.tools import RexiaAIGoogleSearch

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Create an instance of the RexiaAIGoogleSearch tool
google_search = RexiaAIGoogleSearch(api_key=GOOGLE_API_KEY, engine_id=SEARCH_ENGINE_ID)

# Create a dictionary mapping the tool name to its instance
tools = {
    google_search.to_rexiaai_function_call()["name"]: google_search,
}

complex_llm = RexiaAIOpenAI(
    base_url="http://localhost:11434/v1",
    model="llama3.1",
    temperature=0,
    tools=tools,
)

llm = RexiaAIOpenAI(
    base_url="http://localhost:11434/v1",
    model="llama3.1",
    temperature=0,
    tools=tools,
)

# Create agents to populate the agency
agent = Agent(
    llm=llm,
    task="Reflect Agent",
    verbose=True,
)
simple_tool_agent = Agent(
    llm=llm,
    task="Simple Tool Agent",
    workflow=SimpleToolWorkflow,
)
code_tool_agent = Agent(
    llm=llm,
    task="Code Tool Agent",
    workflow=CodeToolWorkflow,
)

# Assign the agents names and descriptions so the agency manager can decide how best to use them.
complex = AgentInfo(
    agent=agent,
    name="Steve Jobs",
    description="A reflect agent for performing complex tasks such as planning.",
)

basic = AgentInfo(
    agent=simple_tool_agent,
    name="Elon Musk",
    description="A simple tool agent equipped with google search.",
)

# Create the Agency with a task and our list of AgentInfos
agency = Agency(
    task="Create a game of snake in Python using object oriented principles.",
    agents=[complex, basic],
    manager_llm=llm,
)

# Generate the response from the agent
response = agency.invoke()

# Print the response
print("Response:", response)
