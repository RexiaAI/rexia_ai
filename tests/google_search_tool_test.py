import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.tools import RexiaAIGoogleSearch

class TestAgent(unittest.TestCase):
    def setUp(self):
        # Retrieve the Google API key and search engine ID from environment variables
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

        # Create an instance of the RexiaAIGoogleSearch tool
        self.google_search = RexiaAIGoogleSearch(api_key=GOOGLE_API_KEY, engine_id=SEARCH_ENGINE_ID)

        # Create a dictionary mapping the tool name to its instance
        tools = {"google_search": self.google_search}

        # Create an instance of the RexiaAI LLM with the specified tools
        self.llm = RexiaAIOpenAI(
            base_url="http://localhost:1234/v1",
            model="lm-studio-server",
            temperature=0,
            tools=tools,
        )

        # Create an instance of the RexiaAI Agent with the specified task and LLM
        self.agent = Agent(
            llm=self.llm,
            task="Use Google to tell me what the weather is like in London on the 12th of June 2024.",
            verbose=True,
        )

    def test_response_format(self):
        response = self.agent.reflect()

        self.assertIsInstance(response, dict)
        expected_keys = ['question', 'answer', 'confidence_score', 'chain_of_reasoning']
        self.assertEqual(set(response.keys()), set(expected_keys))

if __name__ == '__main__':
    unittest.main()