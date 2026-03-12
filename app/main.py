import json
from fastapi import FastAPI, HTTPException
from app.core.llm import call_llm
from app.agents.idea_agent import IdeaAgent
from app.agents.market_agent import MarketResearchAgent

app = FastAPI()

@app.get("/test-llm")
def test_llm():
    raw_output = call_llm(
        system_prompt="You are a startup strategist.",
        user_prompt="Give me one SaaS idea in JSON."
    )
    try:
        parsed = json.loads(raw_output)
        return parsed
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Model did not return valid JSON")
    
@app.get("/generate-idea")
def generate_idea():
    agent = IdeaAgent()
    return agent.generate()

@app.get("/full-analysis")
def full_analysis():
    idea_agent = IdeaAgent()
    market_agent = MarketResearchAgent()

    idea = idea_agent.generate()
    market = market_agent.analyze(idea)

    idea["market_research"] = market["market_research"]

    return idea

from app.orchestrator.venture_orchestrator import VentureOrchestrator

@app.get("/run-venture")
def run_venture():
    orchestrator = VentureOrchestrator()
    return orchestrator.run_pipeline()