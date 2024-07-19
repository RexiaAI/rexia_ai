import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from verification.llm_verification import LLMVerification

class TestRexiaAIOpenAI(unittest.TestCase):
    def setUp(self):
        BASE_URL = "http://localhost:1234/v1"

        self.llm = RexiaAIOpenAI(
            base_url=BASE_URL,
            model="lm-studio",
            temperature=0,
        )
        
        self.llm_verification = LLMVerification(
            base_url=BASE_URL, 
            model="lm-studio",
            temperature=0.0
        )

    def test_response_contains_paris(self):
        TASK = "What is the capital of France?"
        
        response = self.llm.invoke(TASK)
        verified_response = self.llm_verification.verify(
            LLMVerification.get_verification_prompt()
            + "\n\n Task:" + TASK
            + "\n\n Response:" + str(response)
        )
        
        self.assertTrue(verified_response, "Response verification failed")    


if __name__ == "__main__":
    unittest.main()
