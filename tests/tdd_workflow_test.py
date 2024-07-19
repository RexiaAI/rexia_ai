import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.workflows import TDDWorkflow
from rexia_ai.structure import RexiaAIResponse
from verification.llm_verification import LLMVerification

class TestLLMCode:
            @classmethod
            def setUpClass(cls):
                import math
                from typing import Union, List
                cls.math = math
                cls.Union = Union
                cls.List = List
            
            @classmethod
            def test_sum_function(cls, func):
                assert func(5, 7) == 12, "5 + 7 should equal 12"
                assert func(-3, 3) == 0, "-3 + 3 should equal 0"
                assert func(0, 0) == 0, "0 + 0 should equal 0"
                assert func(1.5, 2.5) == 4.0, "1.5 + 2.5 should equal 4.0"
                assert func(-1.5, -2.5) == -4.0, "-1.5 + -2.5 should equal -4.0"

            @classmethod
            def setUpClass(cls):
                import math
                from typing import Union, List
                cls.math = math
                cls.Union = Union
                cls.List = List
            
            @classmethod
            def test_sum_function(cls, func):
                assert func(5, 7) == 12, "5 + 7 should equal 12"
                assert func(-3, 3) == 0, "-3 + 3 should equal 0"
                assert func(0, 0) == 0, "0 + 0 should equal 0"
                assert func(1.5, 2.5) == 4.0, "1.5 + 2.5 should equal 4.0"
                assert func(-1.5, -2.5) == -4.0, "-1.5 + -2.5 should equal -4.0"

            @classmethod
            def test_sum_multiple_numbers(cls, func):
                assert func(1, 2, 3, 4, 5) == 15, "Sum of 1 to 5 should be 15"
                assert func() == 0, "Sum of no arguments should be 0"
                assert func(10) == 10, "Sum of single argument should be the argument itself"

            @classmethod
            def test_sum_with_strings(cls, func):
                assert func("2", "3") == 5, "Sum of '2' and '3' as strings should be 5"
                assert func("-1", "1") == 0, "Sum of '-1' and '1' as strings should be 0"

            @classmethod
            def test_sum_with_lists(cls, func):
                assert func([1, 2, 3], [4, 5]) == 15, "Sum of [1, 2, 3] and [4, 5] should be 15"
                assert func([], []) == 0, "Sum of empty lists should be 0"
                assert func([1.5, 2.5], [3, 4]) == 11, "Sum of [1.5, 2.5] and [3, 4] should be 11"

            @classmethod
            def test_sum_edge_cases(cls, func):
                assert cls.math.isclose(func(1e-10, 1e-10), 2e-10, rel_tol=1e-9), "Sum of very small numbers should be accurate"
                assert func(float('inf'), 1) == float('inf'), "Sum with infinity should be infinity"
                assert cls.math.isnan(func(float('nan'), 1)), "Sum with NaN should be NaN"

            @classmethod
            def test_sum_type_hints(cls, func):
                import inspect
                signature = inspect.signature(func)
                assert signature.return_annotation == cls.Union[int, float], "Return type hint should be Union[int, float]"
                for param in signature.parameters.values():
                    assert param.annotation == cls.Union[int, float, str, cls.List[cls.Union[int, float]]], \
                        "Parameter type hints should be Union[int, float, str, List[Union[int, float]]]"

class TestTDDWorkflow(unittest.TestCase):
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
            temperature=0.0
        )

        self.task = "Create a sum_numbers function to pass the test."
        self.agent = Agent(
            llm=self.llm,
            task=self.task,
            workflow=TDDWorkflow,
            verbose=True,
        )
        
        self.agent.workflow.set_test_class(TestLLMCode)

    def test_tdd_workflow_response(self):
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