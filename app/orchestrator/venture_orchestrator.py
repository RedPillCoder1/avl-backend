from app.agents.idea_agent import IdeaAgent
from app.agents.market_agent import MarketResearchAgent
from app.schemas.venture import VentureModel
from app.agents.critic import CriticAgent


class VentureOrchestrator:
    def __init__(self):
        self.idea_agent = IdeaAgent()
        self.market_agent = MarketResearchAgent()
        self.critic_agent = CriticAgent()

    def run_pipeline(self):
      best_venture = None
      best_score = 0
      feedback = None

      for iteration in range(3):
          idea = self.idea_agent.generate(feedback)
          market = self.market_agent.analyze(idea)
          idea["market_research"] = market

          critique = self.critic_agent.evaluate(idea)
          idea["critique"] = critique

          score = critique["score"]

          if score > best_score:
              best_score = score
              best_venture = idea

          if score >= 8:
              return idea

          # Use critic feedback to improve next iteration
          feedback = "\n".join(critique["improvement_suggestions"])

      return best_venture