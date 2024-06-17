import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.tools import RexiaAIYoutubeVideoAnalysis

class TestAgent(unittest.TestCase):
    def setUp(self):
        # Retrieve the OpenAI API key from the environment variable
        OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

        # Create an instance of the RexiaAIYoutubeVideoAnalysis tool
        self.video_analysis = RexiaAIYoutubeVideoAnalysis(
            vision_model_base_url="https://api.openai.com/v1",
            vision_model="gpt-4o",
            openai_api_key=OPEN_AI_API_KEY,
        )
        tools = {"video_analysis": self.video_analysis}

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
            task="Analyze the provided video and describe the objects, people, and activities present.",
            verbose=True,
        )

    def test_response_format(self):
        result = self.agent.reflect()

        self.assertIsInstance(result, dict)
        expected_keys = ['question', 'answer', 'confidence_score', 'chain_of_reasoning']
        self.assertEqual(set(result.keys()), set(expected_keys))

if __name__ == '__main__':
    unittest.main()