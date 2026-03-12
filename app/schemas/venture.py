from pydantic import BaseModel
from typing import List
from app.schemas.market import MarketResearchModel

class MonetizationModel(BaseModel):
    name: str
    description: str

class VentureModel(BaseModel):
    name: str
    description: str
    problem_statement: str
    target_market: str
    monetization: List[MonetizationModel]
    market_research: MarketResearchModel