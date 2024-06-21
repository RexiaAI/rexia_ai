""" ReXia.AI Google Search Tool - Google Search Tool from langchain_community extended to work more 
consistently with open source models within ReXia.AI. Credit to the original authors who did most of 
the work."""

from langchain_google_community import GoogleSearchAPIWrapper
from ..base import BaseTool


class RexiaAIGoogleSearch(BaseTool):
    """
    Google Search Tool that works with ReXia.AI.

    Attributes
    ----------
    api_key : str
        The API key for Google Search.
    engine_id : str
        The engine ID for Google Search.

    Methods
    -------
    google_search(query: str) -> str:
        Run a query through Google Search and parse the result.
    to_rexiaai_tool() -> list:
        Return the tool as a JSON object for ReXia.AI.
    to_rexiaai_function_call() -> dict:
        Return the tool as a dictionary object for ReXia.AI.
    """

    def __init__(self, api_key: str, engine_id: str):
        """
        Constructs all the necessary attributes for the RexiaAIGoogleSearch object.

        Parameters
        ----------
            api_key : str
                The API key for Google Search.
            engine_id : str
                The engine ID for Google Search.
        """
        super().__init__(
            name="google_search",
            func=self.google_search,
            description="Perform a Google search",
        )
        self.api_key = api_key
        self.engine_id = engine_id
        self.google_search_api = GoogleSearchAPIWrapper(
            google_api_key=api_key, google_cse_id=engine_id
        )

    def google_search(self, query: str) -> str:
        """
        Run a query through Google Search and parse the result.

        Parameters
        ----------
            query : str
                The search query you wish to execute.

        Returns
        -------
            str
                The search result.
        """
        if not query:
            raise ValueError("Query must not be empty")
        return self.google_search_api.run(query)

    def to_rexiaai_tool(self) -> list:
        """
        Return the tool as a JSON object for ReXia.AI.

        Returns
        -------
            list
                The tool as a JSON object.
        """
        tool = [
            {
                "name": "google_search",
                "description": "Perform a Google search",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query you wish to execute"
                            "e.g. 'How to make a cake'",
                        },
                    },
                    "required": ["query"],
                },
            }
        ]

        return tool

    def to_rexiaai_function_call(self) -> dict:
        """
        Return the tool as a dictionary object for ReXia.AI.

        Returns
        -------
            dict
                The tool as a dictionary object.
        """
        function_call = {"name": "google_search"}

        return function_call
