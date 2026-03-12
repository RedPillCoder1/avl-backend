import copy
from app.utils.currency_parser import parse_inr

def apply_improvements(pitch, suggestion):

    new_pitch = copy.deepcopy(pitch)

    burn_change = suggestion.get("burn_change_percent", 0)
    revenue_change = suggestion.get("revenue_growth_percent", 0)

    if burn_change != 0:
        current_burn = parse_inr(pitch.monthly_burn)
        new_burn = current_burn * (1 - abs(burn_change) / 100)
        new_pitch.monthly_burn = new_burn

    if revenue_change != 0:
        current_revenue = parse_inr(pitch.monthly_revenue)
        new_revenue = current_revenue * (1 + revenue_change / 100)
        new_pitch.monthly_revenue = new_revenue

    return new_pitch