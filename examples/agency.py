"""Example agent in ReXia.AI."""

# Import necessary modules
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.agencies import Agency, AgentInfo
from rexia_ai.workflows import SimpleToolWorkflow, CodeToolWorkflow
from rexia_ai.tools import RexiaAIGoogleSearch, RexiaAIAlphaVantageExchangeRate

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Create an instance of the RexiaAIGoogleSearch tool
google_search = RexiaAIGoogleSearch(api_key=GOOGLE_API_KEY, engine_id=SEARCH_ENGINE_ID)
exchange_rate = RexiaAIAlphaVantageExchangeRate(api_key=ALPHA_VANTAGE_API_KEY)

# Create a dictionary mapping the tool name to its instance
tools = {
    google_search.to_rexiaai_function_call()["name"]: google_search,
    exchange_rate.to_rexiaai_function_call()["name"]: exchange_rate,
}

complex_llm = RexiaAIOpenAI(
    base_url="http://localhost:1234/v1",
    model="lm-studio",
    temperature=0,
    tools=tools,
)

llm = RexiaAIOpenAI(
    base_url="http://localhost:1234/v1",
    model="lm-studio",
    temperature=0,
    tools=tools,
)

# Create agents to populate the agency
agent = Agent(
    llm=llm,
    task="Reflect Agent",
    verbose=True,
    use_router=True,
    router_llm=llm,
    complex_llm=complex_llm,
    task_complexity_threshold=60
)
simple_tool_agent = Agent(
    llm=llm,
    task="Simple Tool Agent",
    workflow=SimpleToolWorkflow,
    use_router=True,
    router_llm=llm,
    complex_llm=complex_llm,
    task_complexity_threshold=60
)
code_tool_agent = Agent(
    llm=llm,
    task="Code Tool Agent",
    workflow=CodeToolWorkflow,
    use_router=True,
    router_llm=llm,
    complex_llm=complex_llm,
    task_complexity_threshold=60
)

# Assign the agents names and descriptions so the agency manager can decide how best to use them.
complex = AgentInfo(
    agent=agent,
    name="Steve Jobs",
    description="A reflect agent for performing complex tasks such as planning.",
)

code = AgentInfo(
    agent=code_tool_agent,
    name="Bill Gates",
    description="A code tool agent for creating tools on the fly. Useful for mathemtatical functions.",
)

basic = AgentInfo(
    agent=simple_tool_agent,
    name="Elon Musk",
    description="A simple tool agent equipped with google search and currency exchange.",
)

# Create the Agency with a task and our list of AgentInfos
agency = Agency(
    task="I have $2490, plan a week long trip to Paris that will fit within my budget.",
    agents=[complex, code, basic],
    manager_llm=llm,
)

# Generate the response from the agent
response = agency.invoke()

# Print the response
print("Response:", response)
