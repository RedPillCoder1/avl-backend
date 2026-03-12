from app.agents.base_agent import BaseAgent
from app.schemas.improvement import ImprovementSuggestion


class ImprovementAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            role_description="""
You are an expert startup advisor.

Your job is to suggest improvements to a startup idea
that would increase investor returns and reduce failure risk.

Return JSON only.
"""
        )

    def suggest(self, pitch, metrics, simulation, roi):

        prompt = f"""
Startup:
{pitch}

Metrics:
{metrics}

Simulation:
{simulation}

ROI:
{roi}

Suggest improvements.

Return JSON:

{{
"funding_change": "",
"burn_change_percent": 0,
"revenue_growth_percent": 0,
"reasoning": []
}}

IMPORTANT RULES:
- burn_change_percent must ALWAYS be a POSITIVE number. 25 means reduce burn by 25%.
- revenue_growth_percent must ALWAYS be a POSITIVE number. 50 means grow revenue by 50%.
"""

        raw = self.run(prompt)

        validated = ImprovementSuggestion(**raw)

        return validated.model_dump()