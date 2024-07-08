import unittest
import os
from rexia_ai.tools import RexiaAIQueryKnowledgeBase
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.structure import RexiaAIResponse
from verification.llm_verification import LLMVerification

class TestRexiaAIQueryKnowledgeBase(unittest.TestCase):
    def setUp(self):
        YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")
        BASE_URL = "https://api.01.ai/v1"

        if not YI_LARGE_API_KEY:
            self.skipTest("YI_LARGE_API_KEY not found in environment variables.")

        self.query_knowledge_base = RexiaAIQueryKnowledgeBase(
            api_key=YI_LARGE_API_KEY,
            base_url=BASE_URL,
            model="yi-large",
            temperature=0,
        )
        
        tools = {"query_knowledge_base": self.query_knowledge_base}

        self.llm = RexiaAIOpenAI(
            base_url=BASE_URL,
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
            task="What is the capital of France?",
            verbose=True,
        )

    def test_query_knowledgebase(self):
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
