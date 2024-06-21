import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.tools import RexiaAIYoutubeVideoAnalysis
from rexia_ai.structure import RexiaAIResponse


class TestVideoAnalysisTool(unittest.TestCase):
    def setUp(self):
        # Retrieve the OpenAI API key from the environment variable
        OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
        YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

        if not OPEN_AI_API_KEY:
            self.skipTest("OpenAI API key not found in environment variables.")

        if not YI_LARGE_API_KEY:
            self.skipTest("YI_LARGE_API_KEY not found in environment variables.")

        # Create an instance of the RexiaAIYoutubeVideoAnalysis tool
        self.analyse_video = RexiaAIYoutubeVideoAnalysis(
            vision_model_base_url="https://api.openai.com/v1",
            vision_model="gpt-4o",
            openai_api_key=OPEN_AI_API_KEY,
        )
        tools = {"analyse_video": self.analyse_video}

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
            task="Where is this video showing images of? https://www.youtube.com/watch?v=EEeu7-xJX_c&ab_channel=MinutesofPlaces",
            verbose=True,
        )

    def test_response_format(self):
        response = self.agent.reflect()

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
