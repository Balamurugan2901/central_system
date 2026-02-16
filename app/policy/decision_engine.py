def decide_action(risk_level: str):
    if risk_level == "HIGH":
        return "BLOCK"
    if risk_level == "MEDIUM":
        return "ALERT"
    return "ALLOW"
