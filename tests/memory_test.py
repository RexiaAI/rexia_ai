import unittest
import os
from rexia_ai.tools import RexiaAIGoogleSearch
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.structure import RexiaAIResponse


class TestRexiaAIMemory(unittest.TestCase):
    def setUp(self):
        YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

        if not YI_LARGE_API_KEY:
            self.skipTest("YI_LARGE_API_KEY not found in environment variables.")

        # Create an instance of the RexiaAI LLM
        self.llm = RexiaAIOpenAI(
            base_url="https://api.01.ai/v1",
            model="yi-large",
            temperature=0,
            api_key=YI_LARGE_API_KEY,
        )
        # Create an instance of the RexiaAI Agent with the specified task and LLM
        self.agent = Agent(
            llm=self.llm,
            task="What is the capital of France?",
            verbose=True,
        )

    def test_google_search(self):

        # Generate the response from the agent
        self.agent.invoke()
        response = self.agent.invoke("What is the last question you were asked?")

        # Assert that the response is a RexiaAIResponse
        self.assertIsInstance(
            response,
            RexiaAIResponse,
            f"Expected RexiaAIResponse but got {type(response).__name__}",
        )

        # Assert that response contains the expected answer
        expected_answer = "What is the capital of France?"
        self.assertIn(
            expected_answer,
            response.answer,
            "Response does not contain the expected answer.",
        )


if __name__ == "__main__":
    unittest.main()
