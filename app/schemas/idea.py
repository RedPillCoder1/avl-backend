from pydantic import BaseModel
from typing import List

class MonetizationModel(BaseModel):
    name: str
    description: str


class IdeaModel(BaseModel):
    name: str
    description: str
    problem_statement: str
    target_market: str
    monetization: List[MonetizationModel]