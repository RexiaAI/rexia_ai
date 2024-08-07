"""RexiaAIResponse class for ReXia.AI."""

import json5
from typing import Any, Dict, List, Optional, Union

class RexiaAIResponse:
    """
    Represents the response from an LLM using ReXia.AI.

    Attributes:
        question (str): The question asked to the LLM.
        plan (List[str]): The plan or steps the LLM intends to follow to answer the question.
        answer (Union[List[Union[str, dict]], str]): The answer provided by the LLM. Can be a string or a list of strings/objects for formatted content.
        confidence_score (float): The confidence score of the answer, between 0 and 100 percent.
        chain_of_reasoning (List[str]): The chain of reasoning or steps taken to arrive at the answer.
        tool_calls (List[str]): List of tool calls made by the LLM, if any.
    """

    def __init__(
        self,
        question: str,
        plan: Optional[List[str]] = None,
        answer: Union[List[Union[str, dict]], str] = [],
        confidence_score: float = 0.0,
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
    def from_json(cls, json_data: Union[str, dict]) -> "RexiaAIResponse":
        """
        Create a RexiaAIResponse instance from a JSON string or dictionary.
        Preserves the original formatting of the JSON string.

        Args:
            json_data (Union[str, dict]): The JSON string or dictionary representing the response.

        Returns:
            RexiaAIResponse: An instance of RexiaAIResponse.

        Raises:
            ValueError: If the input is not a valid JSON string or dictionary.
        """

        if isinstance(json_data, str):
            try:
                parsed_data = json5.loads(json_data)
            except:
                raise ValueError("Invalid JSON input")
        elif isinstance(json_data, dict):
            parsed_data = json_data
        
        return cls(
            question=parsed_data.get("question", ""),
            plan=parsed_data.get("plan", []),
            answer=parsed_data.get("answer", []),
            confidence_score=cls._safe_float(parsed_data.get("confidence_score", 0)),
            chain_of_reasoning=parsed_data.get("chain_of_reasoning", []),
            tool_calls=parsed_data.get("tool_calls", []),
        )

    @classmethod
    def _safe_float(cls, value: Any) -> float:
        """
        Safely convert a value to float, returning 0.0 if conversion fails.

        Args:
            value (Any): The value to convert.

        Returns:
            float: The converted float value, or 0.0 if conversion fails.
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def get_formatted_answer(self) -> str:
        """
        Return the formatted answer string.

        Returns:
            str: The formatted answer string.
        """
        return self.answer if isinstance(self.answer, str) else "\n".join(self.answer)

    def __str__(self) -> str:
        """
        Return a string representation of the RexiaAIResponse instance.

        Returns:
            str: The string representation of the instance.
        """
        dict_repr = self.to_dict()
        
        # Use json.dumps for consistent formatting of other fields
        return json5.dumps(dict_repr, indent=4, ensure_ascii=False)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the RexiaAIResponse instance to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the instance.
        """
        return {
            "question": self.question,
            "plan": self.plan,
            "answer": self.answer,  # This will keep the original structure (list or string)
            "confidence_score": self.confidence_score,
            "chain_of_reasoning": self.chain_of_reasoning,
            "tool_calls": self.tool_calls
        }