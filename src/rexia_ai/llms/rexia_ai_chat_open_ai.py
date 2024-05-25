"""The RexiaAIChatOpenAI class, extends ChatOpenAI so we can ensure JSON object responses."""

from langchain_openai import ChatOpenAI

class RexiaAIChatOpenAI(ChatOpenAI):
    """The RexiaAIChatOpenAI class, extends ChatOpenAI so we can ensure JSON object responses."""

    def __init__(self, base_url: str, model: str, api_key: str = ""):
        super().__init__(base_url=base_url, api_key=api_key, model=model)