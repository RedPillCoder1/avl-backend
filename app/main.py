import logging
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.schemas.pitch import StartupPitch
from app.analysis.financial_metrics import compute_financial_metrics
from app.simulation.monte_carlo import run_startup_simulation
from app.agents.decision_agent import VentureDecisionAgent
from app.agents.improvement_agent import ImprovementAgent
from app.analysis.scenario_engine import apply_improvements
from fastapi.middleware.cors import CORSMiddleware

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Autonomous Venture Lab",
    description="AI-driven startup investment analysis platform",
    version="1.0.0"
)



decision_agent = VentureDecisionAgent()
improvement_agent = ImprovementAgent()


# --- Request timing middleware ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 3)
    logger.info(f"{request.method} {request.url.path} | {response.status_code} | {duration}s")
    return response


# --- Global exception handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Autonomous Venture Lab"}


@app.post("/evaluate-startup")
def evaluate_startup(pitch: StartupPitch):

    logger.info(f"Evaluating startup: '{pitch.startup_name}' | Industry: {pitch.industry} | Stage: {pitch.stage} | Ask: {pitch.funding_ask}")

    # --- Current scenario ---
    metrics = compute_financial_metrics(pitch)
    simulation_results, roi_info = run_startup_simulation(pitch)

    logger.info(
        f"Simulation complete | "
        f"fail={round(simulation_results['fail']*100, 1)}% | "
        f"unicorn={round(simulation_results['unicorn']*100, 1)}% | "
        f"mega={round(simulation_results['mega_exit']*100, 1)}% | "
        f"multiple={round(roi_info['expected_multiple'], 2)}x"
    )

    decision = decision_agent.evaluate(pitch, metrics, simulation_results, roi_info)
    logger.info(f"Decision: {decision['recommendation']} | Confidence: {decision['confidence_score']}")

    # --- Improvement scenario ---
    suggestion = improvement_agent.suggest(pitch, metrics, simulation_results, roi_info)
    improved_pitch = apply_improvements(pitch, suggestion)
    improved_metrics = compute_financial_metrics(improved_pitch)
    improved_simulation_results, improved_roi_info = run_startup_simulation(improved_pitch)

    logger.info(
        f"Improved simulation | "
        f"fail={round(improved_simulation_results['fail']*100, 1)}% | "
        f"unicorn={round(improved_simulation_results['unicorn']*100, 1)}% | "
        f"multiple={round(improved_roi_info['expected_multiple'], 2)}x"
    )

    logger.info(f"Evaluation complete for '{pitch.startup_name}'")

    return {
        "current_analysis": {
            "metrics": metrics,
            "simulation": simulation_results,
            "roi": roi_info,
            "decision": decision
        },
        "suggested_improvements": suggestion,
        "improved_analysis": {
            "metrics": improved_metrics,
            "simulation": improved_simulation_results,
            "roi": improved_roi_info
        }
    }