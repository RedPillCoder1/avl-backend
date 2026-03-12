from app.utils.currency_parser import parse_inr


def compute_investor_returns(pitch, simulation_results):

    investment = parse_inr(pitch.funding_ask)
    equity = pitch.equity_offered_percent / 100

    # hypothetical exit values
    moderate_exit_value = 200_00_00_000   # ₹200Cr
    unicorn_value = 5_000_00_00_000       # ₹5000Cr
    mega_exit_value = 50_000_00_00_000    # ₹50000Cr

    investor_returns = {}

    investor_returns["moderate_exit_return"] = moderate_exit_value * equity
    investor_returns["unicorn_return"] = unicorn_value * equity
    investor_returns["mega_exit_return"] = mega_exit_value * equity

    expected_return = (
        simulation_results["moderate_exit"] * investor_returns["moderate_exit_return"] +
        simulation_results["unicorn"] * investor_returns["unicorn_return"] +
        simulation_results["mega_exit"] * investor_returns["mega_exit_return"]
    )

    return {
        "investment": investment,
        "expected_return": expected_return,
        "expected_multiple": expected_return / investment
    }