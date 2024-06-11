""" Rexia AI Google Search Tool - Google Search Tool from langchain_community extended to work more 
consistently with open source models within ReXia.AI. Credit to the original authors who did most of 
the work."""

from langchain_google_community import GoogleSearchAPIWrapper
from ..base import BaseTool


class RexiaAIGoogleSearch(BaseTool):
    """Tool that works with ReXia.AI."""

    api_key: str
    engine_id: str

    def __init__(self, api_key: str, engine_id: str):
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
        """Run query through GoogleSearch and parse result."""
        return self.google_search_api.run(query)

    def to_rexiaai_tool(self):
        """Return the tool as a JSON object for ReXia.AI."""

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

    def to_rexiaai_function_call(self):
        """Return the tool as a dictionary object for ReXia.AI."""
        function_call = {"name": "google_search"}

        return function_call
