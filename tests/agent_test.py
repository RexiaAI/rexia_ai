import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.structure import RexiaAIResponse
from verification.llm_verification import LLMVerification

class TestAgent(unittest.TestCase):
    def setUp(self):
        
        BASE_URL = "http://localhost:1234/v1"

        self.llm = RexiaAIOpenAI(
            base_url=BASE_URL,
            model="lm-studio",
            temperature=0.0,
        )
        self.llm_verification = LLMVerification(
            base_url=BASE_URL,
            model="lm-studio",
            temperature=0.0,
        )

        self.agent = Agent(
            llm=self.llm, task="What is the capital of France?", verbose=False
        )

    def test_response(self):
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
