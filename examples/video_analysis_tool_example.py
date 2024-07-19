"""Example image analysis with RexiaAIImageAnalysis tool."""

# Import necessary modules
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.tools import RexiaAIYoutubeVideoAnalysis

# Retrieve the OpenAI API key from the environment variable
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

# Create an instance of the RexiaAIYoutubeVideoAnalysis tool
analyse_video = RexiaAIYoutubeVideoAnalysis(
    vision_model_base_url="https://api.openai.com/v1",
    vision_model="gpt-4o",
    openai_api_key=OPEN_AI_API_KEY,
)
tools = {"analyse_video": analyse_video}

# Create an instance of the RexiaAI LLM with the specified tools
llm = RexiaAIOpenAI(
    base_url="http://localhost:1234/v1",
    model="lm-studio",
    temperature=0,
)

# Create an instance of the RexiaAI Agent with the specified task and LLM
agent = Agent(
    llm=llm,
    task="Where is this video showing images of? https://www.youtube.com/watch?v=EEeu7-xJX_c&ab_channel=MinutesofPlaces",
    verbose=True,
)

result = agent.invoke()
print(result)
