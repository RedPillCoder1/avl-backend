# Autonomous Venture Lab

**AI-powered startup investment analysis. 10,000 Monte Carlo simulations. Under 1 second.**

AVL takes a startup pitch and tells you whether to invest — with full probabilistic reasoning, not gut feel. Submit funding ask, burn rate, team size, and market size. Get back failure probability, unicorn odds, expected ROI multiple, and an AI agent's decision with transparent reasoning. Then see exactly how the startup's odds change if they reduce burn or grow revenue.

> Live demo: [avl.vercel.app](https://avl.vercel.app) ← *(add after deployment)*

---

## What it does

**Input:** A startup pitch — name, stage, industry, monthly burn, monthly revenue, funding ask, equity, team size, market size.

**Output:**
- Probability of failure, moderate exit, unicorn, and mega exit
- Expected ROI multiple for the investor
- AI investment recommendation: `INVEST` / `CONDITIONAL_INVEST` / `DO_NOT_INVEST`
- Confidence score derived from simulation data (not LLM-generated)
- Full decision reasoning — why this recommendation, what would change it
- An improved scenario: what happens if the startup reduces burn and grows revenue

**Speed:** The full evaluation — two LLM calls + two Monte Carlo runs of 10,000 iterations each — completes in under 1 second, powered by Groq's LPU inference.

---

## How it works

```
Pitch input
    │
    ▼
Financial metrics          runway, burn multiple, implied valuation, market capture
    │
    ▼
Monte Carlo engine         10,000 independent simulations × 10 years
    │                      stage-aware growth, burn caps, survival probability,
    │                      random shocks, exit thresholds
    ▼
Decision Agent             LLM evaluates simulation results
    │                      deterministic confidence score computed in Python
    │                      recommendation rules enforced in system prompt
    ▼
Improvement Agent          suggests burn reduction % and revenue growth %
    │
    ▼
Improved simulation        full 10,000-run re-simulation on modified inputs
    │                      not a multiplier — first-principles recomputation
    ▼
Structured JSON response
```

### Why Monte Carlo over DCF?

Discounted Cash Flow models require precise future projections — impossible for early-stage startups. Monte Carlo embraces uncertainty: run 10,000 scenarios with randomly sampled growth rates, market conditions, and burn trajectories. The output is a probability distribution, not a point estimate. The same startup fails in some scenarios and unicorns in others — that variance is the truth.

### Why 10,000 runs?

At 10,000 runs, the standard error of a 5% probability estimate is ±0.22%. Sufficient precision for investment decisions. 1,000 runs produces too much noise. 100,000 runs adds latency without meaningful accuracy gain.

### Why Groq over OpenAI?

Groq's LPU delivers ~10x faster inference than GPT-4 for structured JSON tasks. AVL makes 2 LLM calls per request — latency compounds. Full evaluation completes in ~0.9s with Groq vs ~8-12s with GPT-4.

---

## Simulation validation

Three profiles were validated to confirm correct probability ordering:

| Profile | Fail | Moderate | Unicorn | Mega | Multiple |
|---|---|---|---|---|---|
| Strong (burn 1.25x, runway 40mo) | 7.0% | 80.5% | 12.4% | 0.4% | 4.9x |
| Borderline (burn 2.25x, runway 22mo) | 44.3% | 50.2% | 5.5% | 0.1% | 2.5x |
| Weak (burn 5.5x, runway 13mo) | 66.2% | 32.1% | 1.7% | 0.0% | 1.1x |

Strong > Borderline > Weak across all metrics. The simulation correctly penalizes high burn and rewards runway and revenue efficiency.

---

## Tech stack

| Layer | Technology |
|---|---|
| API framework | FastAPI + Uvicorn |
| Input validation | Pydantic v2 |
| Simulation engine | Python 3.11+ (custom, no external libraries) |
| LLM inference | Groq API (LLaMA 3) |
| Frontend | Next.js 14 (App Router) |
| Styling | Tailwind CSS v3 |

---

## Project structure

```
app/
├── main.py                  FastAPI app, routes, middleware, logging
├── schemas/
│   ├── pitch.py             StartupPitch input schema + business logic validation
│   ├── decision.py          VentureDecision output schema
│   └── improvement.py       ImprovementSuggestion output schema
├── analysis/
│   ├── financial_metrics.py Runway, burn multiple, implied valuation, market capture
│   └── scenario_engine.py   Applies improvement suggestions to pitch
├── simulation/
│   └── monte_carlo.py       10,000-run simulation engine
├── agents/
│   ├── base_agent.py        Base LLM agent class
│   ├── decision_agent.py    Investment recommendation + reasoning
│   └── improvement_agent.py Actionable improvement suggestions
└── utils/
    └── currency_parser.py   INR parser: 5L → 500,000 | 2Cr → 20,000,000
```

---

## API reference

### `POST /evaluate-startup`

**Request body:**
```json
{
  "startup_name": "DataPulse",
  "description": "B2B SaaS analytics platform",
  "industry": "SaaS",
  "stage": "Series A",
  "currency": "INR",
  "funding_ask": "10Cr",
  "equity_offered_percent": 12,
  "team_size": 8,
  "monthly_burn": "30L",
  "monthly_revenue": "24L",
  "market_size": "800Cr"
}
```

Monetary fields use INR notation: `L` = Lakh (100,000), `Cr` = Crore (10,000,000).

**Response structure:**
```json
{
  "current_analysis": {
    "metrics": { "runway_months": 26.7, "burn_multiple": 1.25, "implied_valuation": "83.3Cr", "market_capture": 0.036 },
    "simulation": { "fail": 0.070, "moderate_exit": 0.805, "unicorn": 0.124, "mega_exit": 0.004 },
    "roi": { "investment": 10000000, "expected_return": 49000000, "expected_multiple": 4.9 },
    "decision": {
      "recommendation": "INVEST",
      "confidence_score": 86,
      "strengths": ["..."],
      "risks": ["..."],
      "decision_reasoning": ["Fail probability of 7.0% is below 40% threshold → INVEST eligible", "..."]
    }
  },
  "suggested_improvements": {
    "burn_change_percent": 20,
    "revenue_growth_percent": 30,
    "reasoning": ["..."]
  },
  "improved_analysis": {
    "metrics": { "runway_months": 57.0, "burn_multiple": 0.96, "..." },
    "simulation": { "fail": 0.023, "moderate_exit": 0.801, "unicorn": 0.159, "mega_exit": 0.017 },
    "roi": { "expected_multiple": 6.1 }
  }
}
```

### `GET /health`
Returns `{"status": "ok"}`. Used for deployment health checks.

---

## Running locally

**Prerequisites:** Python 3.11+, Node.js 18+, a [Groq API key](https://console.groq.com)

### Backend

```bash
git clone https://github.com/RedPillCoder1/avl-backend
cd avl-backend

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

uvicorn app.main:app --reload
# → running at http://localhost:8000
```

### Frontend

```bash
git clone https://github.com/RedPillCoder1/avl-frontend
cd avl-frontend

npm install
npm run dev
# → running at http://localhost:3000
```

---

## Key design decisions

| Decision | Rationale |
|---|---|
| Monte Carlo over DCF | Embraces uncertainty. Produces distributions, not point estimates. |
| Revenue-relative exit thresholds | Scales correctly for any market size. Fixed thresholds fail for diverse inputs. |
| Burn capped at 2× revenue | Prevents exponential burn spiral. Models real startup economic behavior. |
| Stage-aware growth rates | Year 0–2: 20–100% growth. Year 6–9: 5–20%. Matches observed startup S-curves. |
| Deterministic confidence score | Computed in Python from simulation data. LLMs output round numbers — this doesn't. |
| Separate improvement simulation | Re-runs full 10,000 iterations on modified inputs. Not a multiplier. Honest first-principles estimate. |

---

## Known limitations

- **INR only** — no multi-currency support yet
- **Fixed ROI multipliers** — exit returns are hardcoded (fail=0.1×, moderate=2×, unicorn=25×, mega=100×), not derived from simulated revenue at exit
- **No historical calibration** — simulation parameters are based on first-principles reasoning, not regression against real startup outcome data
- **Stateless** — no database persistence. Each request is independent.
- **LLM non-determinism** — improvement suggestions vary across identical calls

---

## License

MIT