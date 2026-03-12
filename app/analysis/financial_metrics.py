from app.utils.currency_parser import parse_inr


def compute_financial_metrics(pitch):
    
    funding_ask = parse_inr(pitch.funding_ask)
    monthly_burn = parse_inr(pitch.monthly_burn)
    monthly_revenue = parse_inr(pitch.monthly_revenue)
    market_size = parse_inr(pitch.market_size)

    equity = pitch.equity_offered_percent / 100

    # Runway in months
    runway_months = funding_ask / monthly_burn if monthly_burn else 0

    # Burn multiple (how efficiently capital turns into revenue)
    burn_multiple = monthly_burn / monthly_revenue if monthly_revenue else float("inf")

    # Implied valuation
    implied_valuation = funding_ask / equity if equity else 0

    # Revenue to market capture
    market_capture = (monthly_revenue * 12) / market_size if market_size else 0

    return {
        "runway_months": runway_months,
        "burn_multiple": burn_multiple,
        "implied_valuation": implied_valuation,
        "market_capture": round(market_capture * 100, 4)
    }