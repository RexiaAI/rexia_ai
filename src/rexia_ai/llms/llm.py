"""LLM class for Open AI compatible endpoints in ReXia.AI."""

from typing import Dict, Optional
from pydantic import Field
from langchain_openai import ChatOpenAI
from ..base import BaseTool


class LLM(ChatOpenAI):
    """
    ReXiaAI LLM class for Open AI compatible endpoints.

    Attributes:
        tools: A dictionary of tools available for the LLM.
    """
    tools: Optional[Dict[str, BaseTool]] = Field(default_factory=dict)

    def __init__(self, base_url: str, model: str, temperature: int, tools: Optional[Dict[str, BaseTool]] = None, api_key: Optional[str] = None):
        """
        Initialize a LLM instance.

        Args:
            base_url: The base URL for the OpenAI API.
            model: The model to use for the LLM.
            temperature: The temperature to use for the LLM.
            tools: A dictionary of tools available for the LLM. Defaults to None.
            api_key: The API key for the OpenAI API. Defaults to None.
        """
        super().__init__(base_url=base_url, model=model, temperature=temperature, api_key=api_key)
        self.tools = tools or {}