from core.rules.base_rule import Rule

class VolatilityRule(Rule):
    def __init__(self, logger, max_volatility=0.2):
        super().__init__(logger)
        self.max_volatility = max_volatility

    def evaluate(self, data) -> float:
        vol = data.get("volatility")
        if vol is None or not isinstance(vol, (int, float)):
            self.last_reason = "volatility missing or invalid"
            return 0.0
        if vol <= self.max_volatility:
            self.last_reason = f"volatility={vol} ≤ {self.max_volatility}"
            return 1.0
        else:
            self.last_reason = f"volatility={vol} > {self.max_volatility}"
            return -1.0

