import json
from app.agents.base_agent import BaseAgent
from app.schemas.market import MarketResearchModel
from pydantic import ValidationError

class MarketResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role_description="""
You are a market research analyst.
You analyze startup ideas and expand them with:
- competitor analysis
- market size validation
- risk factors
You MUST return valid JSON only.
"""
        )

    def analyze(self, idea_json: dict):
      raw_output = self.run(f"""
  Return ONLY this structure:

  {{
    "competitor_types": [],
    "estimated_market_size_range": "",
    "key_risks": []
  }}

  Idea:
  {idea_json}
  """)

      try:
          validated = MarketResearchModel(**raw_output)
          return validated.model_dump()
      except ValidationError as e:
          raise Exception(f"Market schema validation failed: {e}")