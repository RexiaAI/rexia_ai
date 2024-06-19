"""Example usage of the RexiaAIHuggingFace class which provides compatability with standard
Huggingface models for ReXia.AI."""

from rexia_ai.llms import RexiaAIHuggingFace

# Create an instance of the RexiaAIHuggingFace LLM
llm = RexiaAIHuggingFace(
    model_name="microsoft/Phi-3-mini-4k-instruct",
    temperature=0.2,
    use_gpu=True,
    trust_remote_code=True,
)

response = llm.invoke("What is the capital of France?")
print("Response:", response)