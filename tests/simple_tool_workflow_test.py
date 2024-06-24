import unittest
import os
from rexia_ai.tools import RexiaAIGoogleSearch
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.structure import RexiaAIResponse
from rexia_ai.workflows import SimpleToolWorkflow


class TestSimpleToolWorkflow(unittest.TestCase):
    def setUp(self):
        # Retrieve the Google API key and search engine ID from environment variables
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
        YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

        if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
            self.skipTest(
                "Google API key or search engine ID not found in environment variables."
            )

        if not YI_LARGE_API_KEY:
            self.skipTest("YI_LARGE_API_KEY not found in environment variables.")

        # Create an instance of the RexiaAIGoogleSearch tool
        self.google_search = RexiaAIGoogleSearch(
            api_key=GOOGLE_API_KEY, engine_id=SEARCH_ENGINE_ID
        )

        # Create a dictionary mapping the tool name to its instance
        tools = {"google_search": self.google_search}

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
            workflow=SimpleToolWorkflow,
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

        # Assert that the response contains the expected answer
        expected_answer = "Paris"
        self.assertIn(
            expected_answer,
            response.answer,
            "Response does not contain the expected answer.",
        )


if __name__ == "__main__":
    unittest.main()
