import json
from app.core.llm import call_llm


class BaseAgent:
    def __init__(self, role_description: str, max_retries: int = 3):
        self.role_description = role_description
        self.max_retries = max_retries

    def run(self, task: str):
        for attempt in range(self.max_retries):
            raw_output = call_llm(
                system_prompt=self.role_description,
                user_prompt=task
            )

            try:
                return json.loads(raw_output)
            except json.JSONDecodeError:
                if attempt == self.max_retries - 1:
                    raise Exception("Agent failed after retries")