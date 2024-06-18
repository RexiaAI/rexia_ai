"""RexiaAILLMWare class for ReXia.AI."""

from typing import Dict, Optional
from pydantic import Field
from llmware.models import ModelCatalog  
from ..base import BaseTool

class RexiaAILLMWare:
    """
    ReXiaAI LLM class for LLMware compaitibility.

    Attributes:
        tools: A dictionary of tools available for the LLM.
        model: The model used for the LLM.
    """
    tools: Optional[Dict[str, BaseTool]] = Field(default_factory=dict)
    model: ModelCatalog
        
    def __init__(self, model: str, temperature: float, tools: Optional[Dict[str, BaseTool]] = None, use_gpu: bool = False):
        """
        Initialize a LLM instance.

        Args:
            model: The model to use for the LLM.
            temperature: The temperature to use for the LLM.
            tools: A dictionary of tools available for the LLM. Defaults to None.
            use_gpu: A flag to enable GPU usage. Defaults to False.
        """
        try:
            self.model = ModelCatalog().load_model(selected_model=model, temperature=temperature, use_gpu=use_gpu)
        except Exception as e:
            print(f"Error while loading the model: {e}")
            self.model = None

    def invoke(self, query: str, add_context: str = "") -> Optional[str]:
        """
        Perform inference using the language model.

        Args:
            query: The query to perform inference on.
            add_context: Additional context to add to the query. Defaults to an empty string.

        Returns:
            The response from the language model.
        """
        if self.model is None:
            print("Error: Model is not loaded.")
            return None

        try:
            response = self.model.inference(query, add_context=add_context).get('llm_response')
            return response
        except Exception as e:
            print(f"Error while performing inference: {e}")
            return None