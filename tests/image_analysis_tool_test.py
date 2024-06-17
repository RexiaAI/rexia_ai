import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.tools import RexiaAIImageAnalysis

class TestAgent(unittest.TestCase):
    def setUp(self):
        # Retrieve the necessary credentials/keys from environment variables
        IMAGE_ANALYSIS_API_KEY = os.getenv("IMAGE_ANALYSIS_API_KEY")
        IMAGE_ANALYSIS_ENDPOINT = os.getenv("IMAGE_ANALYSIS_ENDPOINT")

        # Create an instance of the RexiaAIImageAnalysis tool
        self.image_analysis = RexiaAIImageAnalysis(api_key=IMAGE_ANALYSIS_API_KEY, endpoint=IMAGE_ANALYSIS_ENDPOINT)

        # Create a dictionary mapping the tool name to its instance
        tools = {"image_analysis": self.image_analysis}

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
            task="Analyze the provided image and describe the objects, people, and activities present.",
            verbose=True,
        )

    def test_response_format(self):
        response = self.agent.reflect()

        self.assertIsInstance(response, dict)
        expected_keys = ['question', 'answer', 'confidence_score', 'chain_of_reasoning']
        self.assertEqual(set(response.keys()), set(expected_keys))

if __name__ == '__main__':
    unittest.main()