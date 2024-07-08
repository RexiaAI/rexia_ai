import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from verification.llm_verification import LLMVerification

class TestRexiaAIOpenAI(unittest.TestCase):
    def setUp(self):
        YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")
        BASE_URL = "https://api.01.ai/v1"

        if not YI_LARGE_API_KEY:
            self.skipTest("YI_LARGE_API_KEY not found in environment variables.")

        self.llm = RexiaAIOpenAI(
            base_url=BASE_URL,
            model="yi-large",
            temperature=0,
            api_key=YI_LARGE_API_KEY,
        )
        
        self.llm_verification = LLMVerification(
            base_url=BASE_URL, 
            api_key=YI_LARGE_API_KEY,
            model="yi-large",
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
