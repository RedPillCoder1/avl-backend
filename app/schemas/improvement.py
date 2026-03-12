from pydantic import BaseModel


class ImprovementSuggestion(BaseModel):

    funding_change: str | None = None
    burn_change_percent: int | None = None
    revenue_growth_percent: int | None = None

    reasoning: list[str]