import unittest
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.llm = RexiaAIOpenAI(
            base_url="http://localhost:1234/v1",
            model="lm-studio-server",
            temperature=0
        )
        self.agent = Agent(llm=self.llm, task="What is the biggest animal to ever live?", verbose=True)

    def test_response_format(self):
        # Generate the response from the agent
        response = self.agent.reflect()

        # Assert that the response is a dictionary
        self.assertIsInstance(response, dict)

        # Assert that the response dictionary contains the expected keys
        expected_keys = ['question', 'answer', 'confidence_score', 'chain_of_reasoning']
        self.assertEqual(set(response.keys()), set(expected_keys))

if __name__ == '__main__':
    unittest.main()