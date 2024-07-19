"""Example usage of the RexiaAIOpenAI class which provides compatability
with OpenAI endpoints in ReXia.AI."""

from rexia_ai.llms import RexiaAIOpenAI

# Create an instance of the RexiaAILLMWare LLM
llm = RexiaAIOpenAI(
    base_url="http://localhost:1234/v1",
    model="lm-studio",
    temperature=0,
    temperature=0.0,
)

response = llm.invoke("What is the capital of France?")

print("Response:", response)
