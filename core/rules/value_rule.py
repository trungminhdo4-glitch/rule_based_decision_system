from core.rules.base_rule import Rule


class ValueRule(Rule):
    def __init__(self, logger, min_value=60):
        super().__init__(logger)
        self.min_value = min_value

    def evaluate(self, data) -> float:
        value = data.get("value")
        if value is None or not isinstance(value, (int, float)):
            self.last_reason = "value missing or invalid"
            return 0.0
        if value >= self.min_value:
            self.last_reason = f"value={value} ≥ {self.min_value}"
            return 1.0
        else:
            self.last_reason = f"value={value} < {self.min_value}"
            return -1.0
