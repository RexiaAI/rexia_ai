"""RexiaAIResponse class for ReXia.AI."""

import json
from typing import List, Optional, Union

class RexiaAIResponse:
    """
    Represents the response from an LLM using ReXia.AI.
    """

    def __init__(
        self,
        question: str,
        plan: Optional[List[str]] = None,
        answer: str = "",
        confidence_score: int = 0,
        chain_of_reasoning: Optional[List[str]] = None,
        tool_calls: Optional[List[str]] = None,
    ):
        self.question = question
        self.plan = plan or []
        self.answer = answer
        self.confidence_score = confidence_score
        self.chain_of_reasoning = chain_of_reasoning or []
        self.tool_calls = tool_calls or []

    @classmethod
    def from_json(cls, json_data: Union[str, dict]):
        """
        Create a RexiaAIResponse instance from a JSON string or dictionary.
        """
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        return cls(
            question=json_data.get("question", ""),
            plan=json_data.get("plan", []),
            answer=json_data.get("answer", ""),
            confidence_score=float(json_data.get("confidence_score", 0)),
            chain_of_reasoning=json_data.get("chain_of_reasoning", []),
            tool_calls=json_data.get("tool_calls", []),
        )

    def to_dict(self) -> dict:
        """
        Convert the RexiaAIResponse instance to a dictionary.
        """
        return {
            "question": self.question,
            "plan": self.plan,
            "answer": self.answer,
            "confidence_score": self.confidence_score,
            "chain_of_reasoning": self.chain_of_reasoning,
            "tool_calls": self.tool_calls,
        }

    def __str__(self) -> str:
        """
        Return a string representation of the RexiaAIResponse instance.
        """
        return json.dumps(self.__dict__, indent=4)