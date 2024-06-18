"""RexiaAIHuggingFace class for ReXia.AI."""

from typing import Dict, Optional
from pydantic import Field
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from ..base import BaseTool


class RexiaAIHuggingFace:
    """
    Hugging Face LLM class for Huggingface compatibility.

    Attributes:
        model_name: The name of the Hugging Face model to use for the LLM.
        temperature: The temperature to use for the LLM.
        tools: A dictionary of tools available for the LLM.
        max_length: The maximum length of the output text.
        truncation: A flag to enable truncation.
        use_gpu: A flag to enable GPU usage.
        trust_remote_code: A flag to trust remote code.
        tokenizer: The tokenizer used for the LLM.
        model: The model used for the LLM.
        pipeline: The pipeline used for the LLM.
        do_sample: A flag to enable sampling.
    """

    model_name: str
    temperature: float
    tools: Optional[Dict[str, BaseTool]] = Field(default_factory=dict)
    max_length: int = 1000
    truncation: bool = True
    use_gpu: bool = False
    trust_remote_code: bool = False
    tokenizer: AutoTokenizer
    model: AutoModelForCausalLM
    generation_pipeline: pipeline
    do_sample: bool = True

    def __init__(
        self,
        model_name: str,
        temperature: float,
        tools: Optional[Dict[str, BaseTool]] = None,
        max_length: int = 1000,
        truncation: bool = True,
        use_gpu: bool = False,
        trust_remote_code: bool = False,
    ):
        """
        Initialize a LLM instance.

        Args:
            model_name: The name of the Hugging Face model to use for the LLM.
            temperature: The temperature to use for the LLM.
            tools: A dictionary of tools available for the LLM. Defaults to None.
            max_length: The maximum length of the output text. Defaults to 100.
            truncation: A flag to enable truncation. Defaults to True.
            use_gpu: A flag to enable GPU usage. Defaults to False.
            trust_remote_code: A flag to trust remote code. Defaults to False.
        """
        self.model_name = model_name
        self.temperature = temperature
        self.tools = tools or {}
        self.max_length = max_length
        self.truncation = truncation
        self.use_gpu = use_gpu
        self.trust_remote_code = trust_remote_code

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=self.trust_remote_code,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name, trust_remote_code=self.trust_remote_code
            )
            self.generation_pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.use_gpu else -1,
            )
            self.do_sample = True
        except Exception as e:
            print(f"Error while loading the model: {e}")
            self.generation_pipeline = None

    def invoke(self, query: str, add_context: str = "") -> Optional[str]:
        """
        Perform inference using the language model.

        Args:
            query: The query to perform inference on.
            add_context: Additional context to add to the query. Defaults to an empty string.

        Returns:
            The response from the language model.
        """
        if self.generation_pipeline is None:
            print("Error: Model is not loaded.")
            return None

        try:
            input_text = add_context + query
            response = self.generation_pipeline(
                input_text,
                temperature=self.temperature,
                do_sample=self.do_sample,
                max_length=self.max_length,
                truncation=self.truncation,
            )[0]["generated_text"]
            return response
        except Exception as e:
            print(f"Error while performing inference: {e}")
            return None
