import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI


class TestRexiaAIOpenAI(unittest.TestCase):
    def setUp(self):
        self.YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

        if not self.YI_LARGE_API_KEY:
            self.skipTest("YI_LARGE_API_KEY not found in environment variables.")

        # Create an instance of the RexiaAI LLM
        self.llm = RexiaAIOpenAI(
            base_url="https://api.01.ai/v1",
            model="yi-large",
            temperature=0,
            api_key=self.YI_LARGE_API_KEY,
        )

    def test_response_contains_paris(self):
        response = self.llm.invoke("What is the capital of France?")
        self.assertIn("Paris", response, "Response does not contain 'Paris'")


if __name__ == "__main__":
    unittest.main()
