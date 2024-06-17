from typing import Dict, Optional
from pydantic import Field
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from ..base import BaseTool

class RexiaAIHuggingFace:
    """
    Hugging Face LLM class for Huggingface compatibility.

    Attributes:
        tools: A dictionary of tools available for the LLM.
    """
    tools: Optional[Dict[str, BaseTool]] = Field(default_factory=dict)

    def __init__(self, model_name: str, temperature: float, tools: Optional[Dict[str, BaseTool]] = None, use_gpu: bool = False, trust_remote_code: bool = False):
        """
        Initialize a LLM instance.

        Args:
            model_name: The name of the Hugging Face model to use for the LLM.
            temperature: The temperature to use for the LLM.
            tools: A dictionary of tools available for the LLM. Defaults to None.
            use_gpu: A flag to enable GPU usage. Defaults to False.
        """
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=trust_remote_code)
            self.model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=trust_remote_code)
            self.pipeline = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer, device=0 if use_gpu else -1)
            self.pipeline.model.config.temperature = temperature
            self.tools = tools or {}
        except Exception as e:
            print(f"Error while loading the model: {e}")
            self.pipeline = None

    def invoke(self, query: str, add_context: str = "") -> Optional[str]:
        """
        Perform inference using the language model.

        Args:
            query: The query to perform inference on.
            add_context: Additional context to add to the query. Defaults to an empty string.

        Returns:
            The response from the language model.
        """
        if self.pipeline is None:
            print("Error: Model is not loaded.")
            return None

        try:
            input_text = add_context + query
            response = self.pipeline(input_text, max_length=1024, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=1)[0]['generated_text']
            return response
        except Exception as e:
            print(f"Error while performing inference: {e}")
            return None