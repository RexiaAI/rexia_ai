# llm.py
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI

class LLamaIndexLLMHandler:
    """Handler for Llama Index Language Models."""

    def create_ollama_llm(self, model, verbose=True, temperature=0.2, timeout=3000, system_prompt=None):
        """Create an Ollama language model."""
        return Ollama(model=model, verbose=verbose, temperature=temperature, request_timeout=timeout, system_prompt=system_prompt)

    def create_openai_llm(self, model, verbose=True, temperature=0.2, api_key=None, system_prompt=None):
        """Create an OpenAI language model."""
        return OpenAI(model=model, verbose=verbose, temperature=temperature, api_key=api_key, system_prompt=system_prompt)