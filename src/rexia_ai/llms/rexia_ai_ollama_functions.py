"""Ollama functions for the Rexia AI module."""

from langchain_experimental.llms.ollama_functions import OllamaFunctions

class ReXiaAIOllamaFunctions(OllamaFunctions):
    """Ollama functions for the Rexia AI module."""
    def __init__(self, model: str = "phi3:14b-instruct", format: str = "json"):
        super().__init__(model=model, format=format)