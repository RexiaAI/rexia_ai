"""Ollama functions for the Rexia AI module."""

from langchain_experimental.llms.ollama_functions import OllamaFunctions

class ReXiaAIOllamaFunctions(OllamaFunctions):
    """Ollama functions for the Rexia AI module."""
    def __init__(self, model: str = "phi3:14b-instruct"):
        super().__init__(model=model)