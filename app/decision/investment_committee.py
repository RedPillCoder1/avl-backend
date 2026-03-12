def make_decision(scores, simulation):

    avg_score = (
        scores["market"]
        + scores["finance"]
        + scores["risk"]
        + scores["strategy"]
    ) / 4

    if avg_score > 7 and simulation["success_probability"] > 0.4:
        return "INVEST"

    if avg_score > 5:
        return "INVEST WITH CAUTION"

    return "PASS"