import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.tools import RexiaAIImageAnalysis

class TestAgent(unittest.TestCase):
    def setUp(self):
        # Retrieve the necessary credentials/keys from environment variables
        OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

        # Create an instance of the RexiaAIImageAnalysis tool
        self.image_analysis = RexiaAIImageAnalysis(
            vision_model_base_url="https://api.openai.com/v1",
            vision_model="gpt-4o",
            api_key=OPEN_AI_API_KEY,
        )

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
            task="Where is this a picture of? https://media.istockphoto.com/id/1465834906/photo/eiffel-tower-against-a-mesmerizing-pink-cloudy-sky-in-paris-france.webp?b=1&s=170667a&w=0&k=20&c=DK4yIG2IpJh-N_ln81vIrXIaqJKa5sQME67TBj9SxCc=",
            verbose=True,
        )

    def test_response_format(self):
        response = self.agent.reflect()

        self.assertIsInstance(response, dict)
        expected_keys = ['question', 'plan', 'answer', 'confidence_score', 'chain_of_reasoning', 'tool_calls']
        self.assertEqual(set(response.keys()), set(expected_keys))

if __name__ == '__main__':
    unittest.main()