from pydantic import BaseModel

class InvestmentAnalysis(BaseModel):
    market_score: int
    financial_score: int
    risk_score: int
    strategy_score: int

    expected_roi: float
    failure_probability: float
    unicorn_probability: float

    recommendation: str