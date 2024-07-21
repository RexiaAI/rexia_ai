from typing import Dict, Optional
from pydantic import Field
from langchain_openai import ChatOpenAI
from ..base import BaseTool
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging

logger = logging.getLogger(__name__)

class APICallError(Exception):
    """Custom exception for API call errors."""
    pass

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
            max_tokens: The maximum number of tokens to generate. Defaults to 4096.
        """
        super().__init__(
            base_url=base_url,
            model=model,
            temperature=temperature,
            api_key=api_key,
            max_tokens=max_tokens,
        )
        self.tools = tools or {}

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=60),
        retry=retry_if_exception_type(APICallError),
        before_sleep=lambda retry_state: logger.info(f"Retrying API call (attempt {retry_state.attempt_number})"),
        reraise=True
    )
    def invoke(self, query: str) -> Optional[str]:
        """
        Perform inference using the language model.

        Args:
            query: The query to perform inference on.

        Returns:
            The response from the language model.

        Raises:
            APICallError: If there's an error in the API call.
        """
        try:
            response = super().invoke(query)
            return response.content
        except Exception as e:
            logger.error(f"API call failed: {str(e)}")
            raise APICallError(f"Failed to invoke API: {str(e)}")