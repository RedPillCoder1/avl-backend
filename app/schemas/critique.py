from pydantic import BaseModel
from typing import List


class CritiqueModel(BaseModel):
    score: int  # 1-10
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]