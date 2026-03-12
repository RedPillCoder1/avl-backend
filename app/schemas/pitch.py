from pydantic import BaseModel, field_validator, model_validator
from typing import Literal
import re


VALID_STAGES = {"Pre-Seed", "Seed", "Series A", "Series B", "Series C"}
VALID_INDUSTRIES = {
    "SaaS", "FinTech", "HealthTech", "EdTech", "Logistics",
    "E-Commerce", "AgriTech", "CleanTech", "DeepTech", "Other"
}
INR_PATTERN = re.compile(r"^\d+(\.\d+)?(L|Cr)$", re.IGNORECASE)


class StartupPitch(BaseModel):

    startup_name: str
    description: str
    industry: str
    stage: str
    currency: Literal["INR"] = "INR"

    funding_ask: str
    equity_offered_percent: float
    team_size: int
    monthly_burn: str
    monthly_revenue: str
    market_size: str

    # --- String field validators ---
    @field_validator("startup_name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("startup_name cannot be empty")
        if len(v) > 100:
            raise ValueError("startup_name must be under 100 characters")
        return v.strip()

    @field_validator("stage")
    def validate_stage(cls, v):
        if v not in VALID_STAGES:
            raise ValueError(f"stage must be one of: {', '.join(VALID_STAGES)}")
        return v

    @field_validator("industry")
    def validate_industry(cls, v):
        if v not in VALID_INDUSTRIES:
            raise ValueError(f"industry must be one of: {', '.join(VALID_INDUSTRIES)}")
        return v

    @field_validator("equity_offered_percent")
    def validate_equity(cls, v):
        if not (1 <= v <= 50):
            raise ValueError("equity_offered_percent must be between 1 and 50")
        return v

    @field_validator("team_size")
    def validate_team(cls, v):
        if not (1 <= v <= 500):
            raise ValueError("team_size must be between 1 and 500")
        return v

    # --- INR format validators ---
    @field_validator("funding_ask", "monthly_burn", "monthly_revenue", "market_size")
    def validate_inr_format(cls, v):
        if not INR_PATTERN.match(v):
            raise ValueError(f"'{v}' is not valid INR format. Use formats like: 5L, 2.5Cr, 100L")
        return v

    # --- Cross-field validation ---
    @model_validator(mode="after")
    def validate_business_logic(self):
        from app.utils.currency_parser import parse_inr

        burn = parse_inr(self.monthly_burn)
        revenue = parse_inr(self.monthly_revenue)
        funding = parse_inr(self.funding_ask)
        market = parse_inr(self.market_size)

        if burn <= 0:
            raise ValueError("monthly_burn must be greater than 0")
        if revenue < 0:
            raise ValueError("monthly_revenue cannot be negative")
        if funding <= 0:
            raise ValueError("funding_ask must be greater than 0")
        if market <= 0:
            raise ValueError("market_size must be greater than 0")
        if funding > market:
            raise ValueError("funding_ask cannot exceed market_size — this is unrealistic")
        if burn > funding:
            raise ValueError("monthly_burn exceeds total funding_ask — runway would be under 1 month")

        return self