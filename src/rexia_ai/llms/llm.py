"""ReXiaAI LLM class."""

from typing import Dict, Optional
from pydantic import Field
from langchain_openai import ChatOpenAI
from ..base import BaseTool

class LLM(ChatOpenAI):
    """ReXiaAI LLM class."""
    tools: Optional[Dict[str, BaseTool]] = Field(default_factory=dict)

    def __init__(self, base_url: str, model: str, temperature: int, tools: Optional[Dict[str, BaseTool]] = None, api_key: Optional[str] = None):
        super().__init__(base_url=base_url, model=model, temperature=temperature, api_key=api_key)
        self.tools = tools or {}
        