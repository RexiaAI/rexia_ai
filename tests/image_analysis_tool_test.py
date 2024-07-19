import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.tools import RexiaAIImageAnalysis
from rexia_ai.structure import RexiaAIResponse
from verification.llm_verification import LLMVerification


class TestImageAnalysisTool(unittest.TestCase):
    def setUp(self):
        OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
        BASE_URL = "http://localhost:1234/v1"

        self.image_analysis = RexiaAIImageAnalysis(
            vision_model_base_url="https://api.openai.com/v1",
            vision_model="gpt-4o",
            api_key=OPEN_AI_API_KEY,
        )

        tools = {"image_analysis": self.image_analysis}

        self.llm = RexiaAIOpenAI(
            base_url=BASE_URL,
            model="lm-studio",
            temperature=0,
            tools=tools,
        )

        self.llm_verification = LLMVerification(
            base_url=BASE_URL, 
            model="lm-studio",
            temperature=0.0
        )

        self.agent = Agent(
            llm=self.llm,
            task="Where is this a picture of? https://media.istockphoto.com/id/1465834906/photo/eiffel-tower-against-a-mesmerizing-pink-cloudy-sky-in-paris-france.webp?b=1&s=170667a&w=0&k=20&c=DK4yIG2IpJh-N_ln81vIrXIaqJKa5sQME67TBj9SxCc=",
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
