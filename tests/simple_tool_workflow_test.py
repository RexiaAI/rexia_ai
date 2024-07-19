import unittest
import os
from rexia_ai.tools import RexiaAIGoogleSearch
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.structure import RexiaAIResponse
from rexia_ai.workflows import SimpleToolWorkflow
from verification.llm_verification import LLMVerification


class TestSimpleToolWorkflow(unittest.TestCase):
    def setUp(self):
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
        BASE_URL = "http://localhost:1234/v1"

        if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
            self.skipTest(
                "Google API key or search engine ID not found in environment variables."
            )

        self.google_search = RexiaAIGoogleSearch(
            api_key=GOOGLE_API_KEY, engine_id=SEARCH_ENGINE_ID
        )

        tools = {"google_search": self.google_search}

        self.llm = RexiaAIOpenAI(
            base_url=BASE_URL,
            model="lm-studio",
            temperature=0,
            tools=tools,
        )
        
        self.llm_verification = LLMVerification(
            base_url=BASE_URL,
            model="lm-studio",
            temperature=0,
        )

        self.agent = Agent(
            llm=self.llm,
            task="What is the capital of France?",
            verbose=True,
            workflow=SimpleToolWorkflow,
        )

    def test_google_search(self):
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
