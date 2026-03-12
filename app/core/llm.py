import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER")
MODEL = os.getenv("LLM_MODEL")

if PROVIDER == "groq":
  client = OpenAI(
    api_key = os.getenv("GROQ_API_KEY"),
    base_url = "https://api.groq.com/openai/v1"
  )
else:
  client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
  )

def call_llm(system_prompt: str, user_prompt: str):
  response = client.chat.completions.create(
    model = MODEL,
    messages=[
            {
              "role": "system", 
              "content": system_prompt + "\nYou MUST respond with valid JSON only. No markdown. No explaination."
            },
            {
              "role": "user", 
              "content": user_prompt
            }
    ],
    temperature=0.2
  )

  return response.choices[0].message.content