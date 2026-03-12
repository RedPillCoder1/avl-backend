from app.agents.base_agent import BaseAgent
from app.schemas.critique import CritiqueModel
from pydantic import ValidationError


class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role_description="""
You are a brutally honest VC evaluating startup ideas.
Score from 1 to 10.
Be analytical and realistic.
Return JSON only.
"""
        )

    def evaluate(self, venture: dict):
        raw_output = self.run(f"""
Evaluate this startup venture.

Return ONLY this structure:

{{
  "score": 0,
  "strengths": [],
  "weaknesses": [],
  "improvement_suggestions": []
}}

Venture:
{venture}
""")

        validated = CritiqueModel(**raw_output)
        return validated.model_dump()