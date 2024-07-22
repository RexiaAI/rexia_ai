import unittest
from rexia_ai.agents import Agent
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.workflows import CollaborationWorkflow
from rexia_ai.structure import RexiaAIResponse
from verification.llm_verification import LLMVerification

class TestCollaborationWorkflow(unittest.TestCase):
    def setUp(self):
        BASE_URL = "http://localhost:1234/v1"
        
        self.llm = RexiaAIOpenAI(
            base_url=BASE_URL,
            model="lm-studio",
            temperature=0,
        )
        
        self.agent = Agent(
            llm=self.llm,
            task="I have £10,000 to invest in the stockmarket, I want to know the best strategy to make the most of my money.",
            workflow=CollaborationWorkflow,
            verbose=True,
        )

        self.llm_verification = LLMVerification(
            base_url=BASE_URL,
            model="lm-studio",
            temperature=0.0,
        )

    def test_collaboration_workflow(self):
        response = self.agent.invoke()
        messages = self.agent.workflow.channel.messages

        verified_response = self.llm_verification.verify(
            LLMVerification.get_verification_prompt()
            + "\n\n Task:" + self.agent.task
            + "\n\n Response:" + str(response)
            + "\n\n Collaboration Chat:\n" + "\n".join(messages)
        )

        self.assertIsInstance(response, RexiaAIResponse)
        self.assertTrue(verified_response, "Response verification failed")

if __name__ == '__main__':
    unittest.main()