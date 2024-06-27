"""ReXia.AI Query Knowledge Base Tool - let's a small local model query a larger model for information or assistance."""

from ..llms import RexiaAIOpenAI

class RexiaAIQueryKnowledgeBase:
    """
    A class to query a knowledge base using ReXia.AI's integration with large language models.

    This class initializes with a specific model and temperature setting, creating an agent
    that can perform tasks by querying the knowledge base.

    Attributes:
        llm (RexiaAIOpenAI): An instance of the RexiaAIOpenAI class, configured with the specified model and temperature.

    Parameters:
        model (str): The identifier of the model to be used for querying the knowledge base.
        temperature (float): The temperature setting for the model, controlling the randomness of the generated responses.

    Methods:
        invoke(task: str) -> str: Invokes the agent with a specified task and returns the response.
    """

    def __init__(self, base_url: str, api_key: str, model: str, temperature: float) -> None:
        """
        Initializes the QueryKnowledgeBase with a specified model and temperature.

        Args:
            base_url (str): The base URL for the large language model API.
            api_key (str): The API key for the large language model API.
            model (str): The model identifier for querying the knowledge base.
            temperature (float): The temperature to control the randomness of model responses.
        """
        self.llm = RexiaAIOpenAI(
            base_url=base_url,
            api_key=api_key,
            model=model,
            temperature=temperature,
        )
        
    def query_knowledge_base(self, query: str) -> str:
        """
        Invokes the llm with a specified query and returns the model's response.

        This method queries the knowledge base with the given query and returns the response.

        Args:
            query (str): The task or query to be sent to the knowledge base.

        Returns:
            str: The response from the knowledge base to the given query.
        """
        response = self.llm.invoke(query)
        
        return response
    
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
                "name": "query_knowledge_base",
                "description": "Query a knowledge base for information or assistance.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query or task to be sent to the knowledge base."
                            "e.g. 'Help me complete this task.'",
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
        function_call = {"name": "query_knowledge_base"}

        return function_call