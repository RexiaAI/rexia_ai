import unittest
from rexia_ai.llms import RexiaAILLMWare

class TestRexiaAILLMWare(unittest.TestCase):
    def setUp(self):
        # Create an instance of the RexiaAILLMWare LLM
        self.llm = RexiaAILLMWare(
            model="llmware/bling-phi-3-gguf",
            temperature=0.0,
            use_gpu=True,
        )

    def test_response_contains_paris(self):
        response = self.llm.invoke("What is the capital of France?")
        self.assertIn("Paris", response, "Response does not contain 'Paris'")

if __name__ == '__main__':
    unittest.main()