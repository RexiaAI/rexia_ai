""" structured output parser for ReXiaAI """

from pydantic import BaseModel

class AnswerSchema(BaseModel):
    """ structured output schema for ReXiaAI """
    question: str
    answer: str
    confidence_score: float
    supporting_evidence: list[str]
    