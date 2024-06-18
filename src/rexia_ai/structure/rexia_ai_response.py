"""RexiaAIResponse class for ReXia.AI."""
from typing import List
from pydantic import BaseModel, Field, model_validator
import json

class RexiaAIResponse(BaseModel):
    """
    Represents the response from an LLM using ReXia.AI.
    """
    question: str
    plan: List[str] = Field(..., description="A list of steps or subtasks to execute the task.")
    answer: str
    confidence_score: int = Field(..., ge=0, le=100, description="Confidence score for the answer (0-100).")
    chain_of_reasoning: List[str] = Field(..., description="A list of reasoning steps or explanations.")
    tool_calls: List[str] = Field(..., description="A list of tool calls or external resources used.")

    @model_validator(pre=True)
    def parse_lists_from_json(cls, values):
        """
        Parse list fields from JSON strings if necessary.
        """
        for field_name, field_value in values.items():
            field_definition = cls.model_fields_set.get(field_name)
            if isinstance(field_value, str) and field_definition and field_definition.outer_type_ == List[str]:
                values[field_name] = cls.parse_json_list(field_value)
        return values

    @classmethod
    def from_json(cls, json_str: str):
        """
        Create a RexiaAIResponse instance from a JSON string.
        """
        data = cls.model_validate(json.loads(json_str), strict=True)
        return data

    @staticmethod
    def parse_json_list(json_str: str) -> List[str]:
        """
        Parse a JSON string into a list of strings.
        """
        return [str(item) for item in json.loads(json_str)]