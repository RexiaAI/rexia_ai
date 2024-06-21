"""RexiaAIOpenAI class for Open AI compatible endpoints in ReXia.AI."""

from typing import Dict, Optional
from pydantic import Field
from langchain_openai import ChatOpenAI
from ..base import BaseTool


class RexiaAIOpenAI(ChatOpenAI):
    """
    ReXiaAI LLM class for Open AI compatible endpoints.

    Attributes:
        tools: A dictionary of tools available for the LLM.
    """

    tools: Optional[Dict[str, BaseTool]] = Field(default_factory=dict)

    def __init__(
        self,
        base_url: str,
        model: str,
        temperature: float,
        tools: Optional[Dict[str, BaseTool]] = None,
        api_key: Optional[str] = None,
        max_tokens: int = 4096,
    ):
        """
        Initialize a LLM instance.

        Args:
            base_url: The base URL for the OpenAI API.
            model: The model to use for the LLM.
            temperature: The temperature to use for the LLM.
            tools: A dictionary of tools available for the LLM. Defaults to None.
            api_key: The API key for the OpenAI API. Defaults to None.
            max_tokens: The maximum number of tokens to generate. Defaults to 1024.
        """
        super().__init__(
            base_url=base_url,
            model=model,
            temperature=temperature,
            api_key=api_key,
            max_tokens=max_tokens,
        )
        self.tools = tools or {}

    def invoke(self, query: str) -> Optional[str]:
        """
        Perform inference using the language model.

        Args:
            query: The query to perform inference on.
            add_context: Additional context to add to the query. Defaults to an empty string.

        Returns:
            The response from the language model.
        """
        response = super().invoke(query).content
        return response
