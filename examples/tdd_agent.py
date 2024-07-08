"""Example agent in ReXia.AI."""

# Import necessary modules
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.workflows import TDDWorkflow

YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

# Create an instance of the RexiaAI LLM
llm = RexiaAIOpenAI(
    base_url="http://localhost:1234/v1",
    model="yi-large",
    temperature=0
)

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


# Create an instance of the RexiaAI Agent with the specified task and LLM. Use task here to give the LLM additional context
# on how it should make the test pass.
agent = Agent(
    llm=llm, task="Create a sum_numbers function to pass the test.", verbose=True, workflow=TDDWorkflow
)

# Set the test
agent.workflow.set_test_class(TestLLMCode)

# Generate the response from the agent
response = agent.invoke()

# Print the response
print("Response:", response)
