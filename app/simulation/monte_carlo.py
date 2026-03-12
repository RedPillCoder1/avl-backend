import random
from app.utils.currency_parser import parse_inr

def run_startup_simulation(pitch, runs=10000):

    # --- Parse inputs ---
    funding = parse_inr(pitch.funding_ask)
    burn = parse_inr(pitch.monthly_burn)
    revenue = parse_inr(pitch.monthly_revenue)
    market = parse_inr(pitch.market_size)
    team_size = getattr(pitch, "team_size", 5)

    outcomes = {"fail": 0, "moderate_exit": 0, "unicorn": 0, "mega_exit": 0}

    # --- Base metrics ---
    runway_months = funding / burn
    monthly_burn_ratio = burn / revenue
    market_capture_estimate = revenue / market

    # --- Quality score (0 to 1) replaces boost ---
    # Combines runway, burn efficiency, market capture into one normalized score
    runway_score   = min(1.0, runway_months / 24)          # 24 months = perfect
    burn_score     = min(1.0, 1 / max(1, monthly_burn_ratio))  # lower burn ratio = better
    market_score   = min(1.0, market_capture_estimate * 2000)   # scales with traction
    team_score     = min(1.0, team_size / 10)
    quality = (runway_score + burn_score + market_score + team_score) / 4  # 0 to 1

    # --- Thresholds relative to starting revenue ---
    base_annual = revenue * 12
    moderate_threshold = base_annual * 4
    unicorn_threshold  = base_annual * 15
    mega_threshold     = base_annual * 40

    for _ in range(runs):
        capital = funding
        current_revenue = revenue
        current_burn = burn
        exited = False

        for year in range(10):

            # Revenue growth: slows over time, better quality = higher floor
            if year < 3:
                growth = random.uniform(1.2 + quality * 0.8, 1.8 + quality * 1.2)
            elif year < 6:
                growth = random.uniform(1.1 + quality * 0.3, 1.4 + quality * 0.4)
            else:
                growth = random.uniform(1.05, 1.2)
            current_revenue *= growth

            # Burn grows slowly, capped at 2x current revenue
            current_burn = min(current_burn * random.uniform(1.01, 1.08), current_revenue * 2)
            capital -= current_burn * 12

            # Out of cash
            if capital <= 0:
                # Survival chance: better quality = easier to raise, later year = more traction
                survival = min(0.85, 0.3 + quality * 0.5 + year * 0.04)
                if random.random() > survival:
                    outcomes["fail"] += 1
                    exited = True
                    break
                capital += current_burn * 18  # bridge round: 18 months runway

            # Random shock failure (market crash, competition, etc.)
            if random.random() < 0.008:
                outcomes["fail"] += 1
                exited = True
                break

            annual_revenue = current_revenue * 12

            # Exit decisions — higher quality = more likely to push for bigger exit
            if annual_revenue >= mega_threshold:
                outcomes["mega_exit"] += 1
                exited = True
                break
            elif annual_revenue >= unicorn_threshold:
                # Low quality startups take the exit, high quality ones push for mega
                if random.random() < (0.5 + quality * 0.3):
                    outcomes["unicorn"] += 1
                    exited = True
                    break
            elif annual_revenue >= moderate_threshold:
                # Low quality startups take the exit, high quality ones push for unicorn
                if random.random() < (0.3 + quality * 0.4):
                    outcomes["moderate_exit"] += 1
                    exited = True
                    break

        if not exited:
            # Survived 10 years — moderate exit
            outcomes["moderate_exit"] += 1

    # --- Probabilities ---
    simulation_results = {k: v / runs for k, v in outcomes.items()}
    total = sum(simulation_results.values())
    assert abs(total - 1.0) < 0.001, f"Probabilities don't sum to 1 — got {total:.4f}"

    # --- ROI ---
    investor_returns = {
        "fail":          funding * 0.1,
        "moderate_exit": funding * 2.0,
        "unicorn":       funding * 25.0,
        "mega_exit":     funding * 100.0
    }

    expected_return = sum(
        simulation_results[k] * investor_returns[k] for k in outcomes
    )

    roi_info = {
        "investment":       funding,
        "expected_return":  expected_return,
        "expected_multiple": expected_return / funding
    }

    return simulation_results, roi_info