import unittest
from rexia_ai.llms import RexiaAIOpenAI

class TestRexiaAIOpenAI(unittest.TestCase):
    def setUp(self):
        # Create an instance of the RexiaAIOpenAI LLM
        self.llm = RexiaAIOpenAI(
            base_url="http://localhost:1234/v1",
            model="llmware/bling-phi-3-gguf",
            api_key="lm-studio",
            temperature=0.0,
        )

    def test_response_contains_paris(self):
        response = self.llm.invoke("What is the capital of France?")
        self.assertIn("Paris", response, "Response does not contain 'Paris'")

if __name__ == '__main__':
    unittest.main()