from app.schemas.pitch import StartupPitch
from app.analysis.financial_metrics import compute_financial_metrics
from app.simulation.monte_carlo import run_startup_simulation
from app.analysis.investor_returns import compute_investor_returns
from app.agents.decision_agent import VentureDecisionAgent


pitch = StartupPitch(
    startup_name="EcoCycle",
    description="AI recycling platform",
    industry="Climate Tech",
    stage="Seed",
    funding_ask="10Cr",
    equity_offered_percent=10,
    team_size=8,
    monthly_burn="40L",
    monthly_revenue="8L",
    market_size="500Cr"
)

metrics = compute_financial_metrics(pitch)

simulation = run_startup_simulation(pitch)

roi = compute_investor_returns(pitch, simulation)

agent = VentureDecisionAgent()

decision = agent.evaluate(pitch, metrics, simulation, roi)

print(decision)