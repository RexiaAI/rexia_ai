import unittest
from rexia_ai.llms import RexiaAIHuggingFace


class TestRexiaAIHuggingFace(unittest.TestCase):
    def setUp(self):
        # Create an instance of the RexiaAIHuggingFace LLM
        self.llm = RexiaAIHuggingFace(
            model_name="microsoft/Phi-3-mini-4k-instruct",
            temperature=0.2,
            use_gpu=True,
            trust_remote_code=True,
        )

    def test_response_contains_paris(self):
        response = self.llm.invoke("What is the capital of France?")
        self.assertIn("Paris", response, "Response does not contain 'Paris'")


if __name__ == "__main__":
    unittest.main()
