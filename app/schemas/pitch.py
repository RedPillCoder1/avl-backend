from pydantic import BaseModel

class StartupPitch(BaseModel):
    startup_name: str
    description: str
    industry: str
    stage: str  # pre-seed, seed, series-a

    funding_ask_usd: float
    equity_offered_percent: float

    team_size: int
    monthly_burn_usd: float
    monthly_revenue_usd: float

    market_size_usd: float