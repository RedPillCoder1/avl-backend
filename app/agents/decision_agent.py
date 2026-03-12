from app.agents.base_agent import BaseAgent
from app.schemas.decision import VentureDecision


class VentureDecisionAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            role_description="""
You are a senior venture capital partner.

Your job is to evaluate startup investment opportunities using
financial metrics, simulation results, and investor ROI analysis.

Return structured JSON only.

Recommendation must be one of:
INVEST
CONDITIONAL_INVEST
DO_NOT_INVEST

IMPORTANT RULES for recommendation:
- fail > 60% → MUST be DO_NOT_INVEST
- fail 40-60% → MUST be CONDITIONAL_INVEST  
- fail < 40% → can be INVEST
- Never recommend INVEST when expected_multiple < 1.5x
"""
        )

    def evaluate(self, pitch, metrics, simulation, roi):

      upside_prob = simulation.get("unicorn", 0) + simulation.get("mega_exit", 0)
      confidence_score = min(95, round(40 + (upside_prob * 200) + (metrics.get("runway_months", 0) / 2)))

      # ADD THIS BLOCK:
      fail_prob = simulation.get("fail", 0)
      if fail_prob > 0.6:
          rec_reason = f"Fail probability of {round(fail_prob*100, 1)}% exceeds 60% threshold → DO_NOT_INVEST"
      elif fail_prob > 0.4:
          rec_reason = f"Fail probability of {round(fail_prob*100, 1)}% is between 40–60% → CONDITIONAL_INVEST"
      else:
          rec_reason = f"Fail probability of {round(fail_prob*100, 1)}% is below 40% → INVEST eligible"

      prompt = f"""
  Evaluate the following startup.

  Startup:
  {pitch}

  Financial Metrics:
  {metrics}

  Simulation Results:
  {simulation}

  Investor ROI:
  {roi}

  IMPORTANT: You must use exactly {confidence_score} as the confidence_score. Do not change it.
  IMPORTANT: First entry of decision_reasoning MUST be exactly: "{rec_reason}"

  Return JSON:

  {{
  "recommendation": "",
  "confidence_score": {confidence_score},
  "strengths": [],
  "risks": [],
  "suggested_changes": [],
  "decision_reasoning": [
      "{rec_reason}",
      "explain which metric most drove this decision",
      "explain the biggest risk factor",
      "explain what would change the recommendation"
  ]
  }}
  """

      raw = self.run(prompt)
      validated = VentureDecision(**raw)
      return validated.model_dump()