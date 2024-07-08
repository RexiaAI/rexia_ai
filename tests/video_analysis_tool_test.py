import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.tools import RexiaAIYoutubeVideoAnalysis
from rexia_ai.structure import RexiaAIResponse
from verification.llm_verification import LLMVerification


class TestVideoAnalysisTool(unittest.TestCase):
    def setUp(self):
        OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
        YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")
        BASE_URL = "https://api.01.ai/v1"

        if not OPEN_AI_API_KEY:
            self.skipTest("OpenAI API key not found in environment variables.")

        if not YI_LARGE_API_KEY:
            self.skipTest("YI_LARGE_API_KEY not found in environment variables.")

        self.analyse_video = RexiaAIYoutubeVideoAnalysis(
            vision_model_base_url="https://api.openai.com/v1",
            vision_model="gpt-4o",
            openai_api_key=OPEN_AI_API_KEY,
        )
        tools = {"analyse_video": self.analyse_video}

        self.llm = RexiaAIOpenAI(
            base_url= "https://api.01.ai/v1",
            model="yi-large",
            temperature=0,
            api_key=YI_LARGE_API_KEY,
            tools=tools,
        )
        
        self.llm_verification = LLMVerification(
            base_url=BASE_URL, 
            api_key=YI_LARGE_API_KEY,
            model="yi-large",
            temperature=0.0
        )

        self.agent = Agent(
            llm=self.llm,
            task="Where is this video showing images of? https://www.youtube.com/watch?v=EEeu7-xJX_c&ab_channel=MinutesofPlaces",
            verbose=True,
        )

    def test_response_format(self):
        response = self.agent.invoke()
        messages = self.agent.workflow.channel.messages
        verified_response = self.llm_verification.verify(
            LLMVerification.get_verification_prompt()
            + "\n\n Task:" + self.agent.task
            + "\n\n Response:" + str(response)
            + "\n\n Collaboration Chat:\n" + "\n".join(messages)
        )

        self.assertIsInstance(
            response,
            RexiaAIResponse,
            f"Expected RexiaAIResponse but got {type(response).__name__}",
        )

        self.assertTrue(verified_response, "Response verification failed")

if __name__ == "__main__":
    unittest.main()
