from core.rules.base_rule import Rule

class RiskRule(Rule):
    def __init__(self, logger, max_risk=0.3):
        super().__init__(logger)
        self.max_risk = max_risk

    def evaluate(self, data) -> float:
        risk = data.get("risk")
        if risk is None or not isinstance(risk, (int, float)):
            self.last_reason = "risk missing or invalid"
            return 0.0
        if risk <= self.max_risk:
            self.last_reason = f"risk={risk} ≤ {self.max_risk}"
            return 1.0
        else:
            self.last_reason = f"risk={risk} > {self.max_risk}"
            return -1.0
