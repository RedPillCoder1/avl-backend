from pydantic import BaseModel
from typing import List


class MarketResearchModel(BaseModel):
    competitor_types: List[str]
    estimated_market_size_range: str
    key_risks: List[str]