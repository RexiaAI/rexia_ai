"""RexiaAIResponse class for ReXia.AI."""

import json
import re
from typing import Any, List, Optional, Union
from json.decoder import JSONDecodeError


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
    def from_json(cls, json_data: Union[str, dict]) -> 'RexiaAIResponse':
        """
        Create a RexiaAIResponse instance from a JSON string or dictionary.
        Attempts to fix common JSON errors and extract valid JSON from text.
        """
        if isinstance(json_data, str):
            json_data = cls._extract_and_fix_json(json_data)
        
        if not isinstance(json_data, dict):
            raise ValueError("Input must be a JSON string or a dictionary.")

        return cls(
            question=json_data.get("question", ""),
            plan=json_data.get("plan", []),
            answer=json_data.get("answer", ""),
            confidence_score=cls._safe_float(json_data.get("confidence_score", 0)),
            chain_of_reasoning=json_data.get("chain_of_reasoning", []),
            tool_calls=json_data.get("tool_calls", []),
        )

    @classmethod
    def _extract_and_fix_json(cls, text: str) -> dict:
        """
        Extract JSON from text, remove any prefixes or suffixes, and attempt to fix common JSON errors.
        """
        # Remove common prefixes and suffixes
        text = cls._clean_text(text)

        # Try to find JSON object in the text
        json_str = cls._find_json_object(text)

        # Attempt to parse JSON, fixing errors if necessary
        return cls._parse_and_fix_json(json_str)

    @classmethod
    def _clean_text(cls, text: str) -> str:
        """
        Remove common prefixes, suffixes, and extraneous whitespace.
        """
        # Remove everything before the first '{' and after the last '}'
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            text = text[start:end+1]
        
        # Remove any remaining newlines and extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    @classmethod
    def _find_json_object(cls, text: str) -> str:
        """
        Find and extract the first complete JSON object from the text.
        """
        # This pattern matches a JSON object, including nested objects and arrays
        pattern = r'\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}'
        json_match = re.search(pattern, text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in the input string.")
        return json_match.group()

    @classmethod
    def _parse_and_fix_json(cls, json_str: str) -> dict:
        """
        Attempt to parse JSON, fixing common errors if necessary.
        """
        try:
            return json.loads(json_str)
        except JSONDecodeError:
            fixed_json_str = cls._fix_json_errors(json_str)
            return json.loads(fixed_json_str)

    @classmethod
    def _fix_json_errors(cls, json_str: str) -> str:
        """
        Attempt to fix common JSON errors.
        """
        # Replace single quotes with double quotes
        json_str = re.sub(r"(?<!\\)'", '"', json_str)

        # Add quotes to unquoted keys
        json_str = re.sub(r'(\w+)(?=\s*:)', r'"\1"', json_str)

        # Remove trailing commas in objects and arrays
        json_str = re.sub(r',\s*([\]}])', r'\1', json_str)

        # Escape unescaped quotes within string values
        json_str = re.sub(r'(?<!\\)"(?=.*":)', r'\"', json_str)

        # Handle boolean and null values
        json_str = re.sub(r'\btrue\b', 'true', json_str, flags=re.IGNORECASE)
        json_str = re.sub(r'\bfalse\b', 'false', json_str, flags=re.IGNORECASE)
        json_str = re.sub(r'\bnull\b', 'null', json_str, flags=re.IGNORECASE)

        return json_str

    @classmethod
    def _safe_float(cls, value: Any) -> float:
        """
        Safely convert a value to float, returning 0.0 if conversion fails.
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

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
