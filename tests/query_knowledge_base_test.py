import unittest
import os
from rexia_ai.tools import RexiaAIQueryKnowledgeBase
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.structure import RexiaAIResponse


class TestRexiaAIQueryKnowledgeBase(unittest.TestCase):
    def setUp(self):
        # Retrieve the YI_LARGE_API_KEY from environment variables
        YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")
        YI_LARGE_BASE_URL = "https://api.01.ai/v1"

        if not YI_LARGE_API_KEY:
            self.skipTest("YI_LARGE_API_KEY not found in environment variables.")

        # Create an instance of the RexiaAIGoogleSearch tool
        self.query_knowledge_base = RexiaAIQueryKnowledgeBase(
            api_key=YI_LARGE_API_KEY,
            base_url=YI_LARGE_BASE_URL,
            model="yi-large",
            temperature=0,
        )

        # Create a dictionary mapping the tool name to its instance
        tools = {"query_knowledge_base": self.query_knowledge_base}

        # Create an instance of the RexiaAI LLM
        self.llm = RexiaAIOpenAI(
            base_url="https://api.01.ai/v1",
            model="yi-large",
            temperature=0,
            api_key=YI_LARGE_API_KEY,
            tools=tools,
        )

        # Create an instance of the RexiaAI Agent with the specified task and LLM
        self.agent = Agent(
            llm=self.llm,
            task="What is the capital of France?",
            verbose=True,
        )

    def test_google_search(self):

        # Generate the response from the agent
        response = self.agent.invoke()

        # Assert that the response is a RexiaAIResponse
        self.assertIsInstance(
            response,
            RexiaAIResponse,
            f"Expected RexiaAIResponse but got {type(response).__name__}",
        )

if __name__ == "__main__":
    unittest.main()
