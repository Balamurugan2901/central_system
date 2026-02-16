def classify_risk(score: float) -> str:
    if score < 3:
        return "LOW"
    elif score < 7:
        return "MEDIUM"
    else:
        return "HIGH"
