from pydantic import BaseModel


class VentureDecision(BaseModel):

    recommendation: str
    confidence_score: int
    strengths: list[str]
    risks: list[str]
    suggested_changes: list[str]
    decision_reasoning: list[str]