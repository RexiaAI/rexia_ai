""" Rexia AI Google Search Tool - Google Search Tool that works with OllamaFunctions"""

from langchain_google_community import GoogleSearchAPIWrapper


class RexiaAIGooleSearch(GoogleSearchAPIWrapper):
    """Tool that works with OllamaFunctions."""
    def google_search(self, query: str) -> str:
        """Run query through GoogleSearch and parse result."""
        super().run(query)

    def to_ollama_tool(self):
        """Return the tool as a JSON object for OllamaFunctions."""

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

    def to_ollama_function_call(self):
        """Return the tool as a JSON object for OllamaFunctions."""
        function_call = {"name": "google_search"}

        return function_call
