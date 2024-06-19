"""Example usage of the RexiaAILLMWare class which provides compatability with LLMWare for ReXia.AI."""

from rexia_ai.llms import RexiaAILLMWare

# Create an instance of the RexiaAILLMWare LLM
llm = RexiaAILLMWare(
    model="llmware/bling-phi-3-gguf",
    temperature=0.0,
    use_gpu=True,
)

response = llm.invoke("What is the capital of France?")

print("Response:", response)