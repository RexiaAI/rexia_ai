"""Example image analysis with RexiaAIImageAnalysis tool. You need a vision or multimodal model to use it."""

# Import necessary modules
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.tools import RexiaAIImageAnalysis

# Retrieve the OpenAI API key from the environment variable
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

# Create an instance of the RexiaAIImageAnalysis tool
image_analysis = RexiaAIImageAnalysis(
    vision_model_base_url="https://api.openai.com/v1",
    vision_model="gpt-4o",
    api_key=OPEN_AI_API_KEY,
)

# Create a dictionary mapping the tool name to its instance
tools = {"image_analysis": image_analysis}

# Create an instance of the RexiaAI LLM with the specified tools
llm = RexiaAIOpenAI(
    base_url="https://api.01.ai/v1",
    model="yi-large",
    temperature=0,
    api_key=YI_LARGE_API_KEY,
    tools=tools,
    max_tokens=4000,
)

# Create an instance of the RexiaAI Agent with the specified task and LLM
agent = Agent(
    llm=llm,
    task="Where is this a picture of? https://media.istockphoto.com/id/1465834906/photo/eiffel-tower-against-a-mesmerizing-pink-cloudy-sky-in-paris-france.webp?b=1&s=170667a&w=0&k=20&c=DK4yIG2IpJh-N_ln81vIrXIaqJKa5sQME67TBj9SxCc=",
    verbose=True,
)

# Generate the response from the agent
response = agent.reflect()

# Print the response
print("Response:", response)
