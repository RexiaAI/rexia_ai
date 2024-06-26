import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.tools import RexiaAIImageAnalysis
from rexia_ai.structure import RexiaAIResponse


class TestImageAnalysisTool(unittest.TestCase):
    def setUp(self):
        # Retrieve the necessary credentials/keys from environment variables
        OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
        YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

        # Create an instance of the RexiaAIImageAnalysis tool
        self.image_analysis = RexiaAIImageAnalysis(
            vision_model_base_url="https://api.openai.com/v1",
            vision_model="gpt-4o",
            api_key=OPEN_AI_API_KEY,
        )

        # Create a dictionary mapping the tool name to its instance
        tools = {"image_analysis": self.image_analysis}

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
            task="Where is this a picture of? https://media.istockphoto.com/id/1465834906/photo/eiffel-tower-against-a-mesmerizing-pink-cloudy-sky-in-paris-france.webp?b=1&s=170667a&w=0&k=20&c=DK4yIG2IpJh-N_ln81vIrXIaqJKa5sQME67TBj9SxCc=",
            verbose=True,
        )

    def test_response_format(self):
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
