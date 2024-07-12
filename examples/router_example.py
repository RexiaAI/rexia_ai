"""Example agent with a router in ReXia.AI."""

# Import necessary modules
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent

YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

# Create an instance of the RexiaAI LLM for the base model.
base_llm = RexiaAIOpenAI(
    base_url="http://localhost:1234/v1",
    model="yi-1.5",
    temperature=0,
)

# Create an instance of the RexiaAI LLM for the router model.
router_llm = RexiaAIOpenAI(
    base_url="http://localhost:1234/v1",
    model="yi-1.5",
    temperature=0,
)

# Create an instance of the RexiaAI LLM for the complex model
complex_llm = RexiaAIOpenAI(
    base_url="https://api.01.ai/v1",
    model="yi-large",
    temperature=0,
    api_key=YI_LARGE_API_KEY,
)


# Create an instance of the RexiaAI Agent with a simple task
agent = Agent(
    llm=base_llm, # The llm for less basic tasks, for instance a local instance of Llama 3
    task="What is the capital of France?",
    verbose=True,
    use_router=True, # Set this to enable the router
    router_llm=router_llm, # You must add a router llm to use routing
    complex_llm=complex_llm, # The llm for more complex tasks, e.g. Yi-Large, GPT-4o, Claude 3.5, etc
    task_complexity_threshold=50 # This is the current default value.
)

# Generate the response from the agent
response = agent.invoke()

# Print the response
print("Response:", response)

response = agent.invoke(task="""Write a 500-word explanation of how photosynthesis works in plants, 
             including the light-dependent and light-independent reactions. Describe the role of chlorophyll, 
             the importance of water and carbon dioxide, and how the process produces glucose and oxygen. 
             Then, discuss how this process impacts the global carbon cycle and its significance for life on Earth.""")

print("Response:", response)
