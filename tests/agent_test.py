import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.structure import RexiaAIResponse


class TestAgent(unittest.TestCase):
    def setUp(self):
        YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

        # Create an instance of the RexiaAI LLM
        self.llm = RexiaAIOpenAI(
            base_url="https://api.01.ai/v1",
            model="yi-large",
            temperature=0,
            api_key=YI_LARGE_API_KEY,
        )
        self.agent = Agent(
            llm=self.llm, task="What is the biggest animal to ever live?", verbose=False
        )

    def test_response_format(self):
        # Generate the response from the agent
        response = self.agent.invoke()

        # Assert that the response is a RexiaAIResponse
        self.assertIsInstance(
            response,
            RexiaAIResponse,
            f"Expected RexiaAIResponse but got {type(response).__name__}",
        )

        # Assert that the response contains the expected answer
        self.assertIn(
            "blue whale",
            response.answer,
            "Response does not contain the expected answer.",
        )


if __name__ == "__main__":
    unittest.main()
