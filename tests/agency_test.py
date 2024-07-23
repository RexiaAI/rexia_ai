import unittest
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.agencies import Agency, AgentInfo
from rexia_ai.workflows import SimpleToolWorkflow, CodeToolWorkflow
from verification.llm_verification import LLMVerification

class TestAgency(unittest.TestCase):
    def setUp(self):
        BASE_URL = "http://localhost:1234/v1"

        self.llm = RexiaAIOpenAI(
            base_url=BASE_URL,
            model="lm-studio",
            temperature=0.0,
        )
        self.llm_verification = LLMVerification(
            base_url=BASE_URL,
            model="lm-studio",
            temperature=0.0,
        )

        # Create agents
        reflect_agent = Agent(
            llm=self.llm,
            task="Reflect Agent",
            verbose=False,
            use_router=True,
            router_llm=self.llm,
            complex_llm=self.llm,
            task_complexity_threshold=60
        )
        simple_tool_agent = Agent(
            llm=self.llm,
            task="Simple Tool Agent",
            workflow=SimpleToolWorkflow,
            use_router=True,
            router_llm=self.llm,
            complex_llm=self.llm,
            task_complexity_threshold=60
        )
        code_tool_agent = Agent(
            llm=self.llm,
            task="Code Tool Agent",
            workflow=CodeToolWorkflow,
            use_router=True,
            router_llm=self.llm,
            complex_llm=self.llm,
            task_complexity_threshold=60
        )

        # Create AgentInfo instances
        self.agents = [
            AgentInfo(agent=reflect_agent, name="Steve Jobs", description="A reflect agent for performing complex tasks such as planning."),
            AgentInfo(agent=simple_tool_agent, name="Elon Musk", description="A simple tool agent equipped with google search and currency exchange."),
            AgentInfo(agent=code_tool_agent, name="Bill Gates", description="A code tool agent for creating tools on the fly. Useful for mathematical functions.")
        ]

        self.agency = Agency(
            task="Plan a week-long trip to Paris with a budget of $2490.",
            agents=self.agents,
            manager_llm=self.llm
        )

    def test_agency_response(self):
        response = self.agency.invoke()
        
        # Get messages from the collaboration channel
        messages = self.agency.manager.collaboration_channel.messages
        
        verified_response = self.llm_verification.verify(
            LLMVerification.get_verification_prompt()
            + "\n\n Task:" + self.agency.task
            + "\n\n Response:" + str(response)
            + "\n\n Collaboration Chat:\n" + "\n".join(messages)
        )

        self.assertIsInstance(
            response,
            str,
            f"Expected str but got {type(response).__name__}",
        )

        self.assertTrue(verified_response, "Response verification failed")

if __name__ == "__main__":
    unittest.main()