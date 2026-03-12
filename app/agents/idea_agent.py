from app.agents.base_agent import BaseAgent
from app.schemas.idea import IdeaModel
from pydantic import ValidationError
import json


class IdeaAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role_description="""
You are an elite startup ideation agent.
You think like a top-tier YC founder.
You MUST return valid JSON only. No extra fields. No markdown.
Return EXACTLY the fields requested. Do not add new keys.
"""
        )

    def generate(self, feedback: str | None = None):
      if feedback:
          prompt = f"""
  Improve the following startup idea based on this feedback:

  Feedback:
  {feedback}

  Return the improved idea in this exact JSON structure:

  {{
    "name": "",
    "description": "",
    "problem_statement": "",
    "target_market": "",
    "monetization": [
      {{
        "name": "",
        "description": ""
      }}
    ]
  }}
  """
      else:
          prompt = """
Generate a high-potential startup idea with this exact structure:

{
  "name": "",
  "description": "",
  "problem_statement": "",
  "target_market": "",
  "monetization": [
    {
      "name": "",
      "description": ""
    }
  ]
}
"""

      raw_output = self.run(prompt)

      if isinstance(raw_output, str):
          raw_output = raw_output.strip()

          # If wrapped in markdown-style quotes or accidental wrapping
          if raw_output.startswith('"') and raw_output.endswith('"'):
              raw_output = raw_output[1:-1]

          raw_output = json.loads(raw_output)

      print("PARSED OUTPUT:", raw_output)

      validated = IdeaModel(**raw_output)
      return validated.model_dump()