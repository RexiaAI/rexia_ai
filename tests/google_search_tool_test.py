import unittest
import os
from rexia_ai.tools import RexiaAIGoogleSearch
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent

class TestRexiaAIGoogleSearch(unittest.TestCase):
    def setUp(self):
        # Retrieve the Google API key and search engine ID from environment variables
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

        if not self.GOOGLE_API_KEY or not self.SEARCH_ENGINE_ID:
            self.skipTest("Google API key or search engine ID not found in environment variables.")

        # Create an instance of the RexiaAIGoogleSearch tool
        self.google_search = RexiaAIGoogleSearch(api_key=self.GOOGLE_API_KEY, engine_id=self.SEARCH_ENGINE_ID)
        
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
            task="Where is this a picture of? https://media.istockphoto.com/id/1465834906/photo/eiffel-tower-against-a-mesmerizing-pink-cloudy-sky-in-paris-france.webp?b=1&s=170667a&w=0&k=20&c=DK4yIG2IpJh-N_ln81vIrXIaqJKa5sQME67TBj9SxCc=",
            verbose=True,
        )

    def test_google_search(self):
        query = "What is the capital of France?"
        
        # Generate the response from the agent
        response = self.agent.reflect()

        # Assert that the response is a dictionary
        self.assertIsInstance(response, dict, f"Expected dict but got {type(response).__name__}")

        # Assert that the response dictionary contains the expected keys
        expected_keys = ['question', 'plan', 'answer', 'confidence_score', 'chain_of_reasoning', 'tool_calls']
        self.assertSetEqual(set(response.keys()), set(expected_keys), f"Missing keys in response: {set(expected_keys) - set(response.keys())}")

if __name__ == '__main__':
    unittest.main()