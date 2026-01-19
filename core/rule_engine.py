class RuleEngine:
    def __init__(self, rules_with_weights, logger):
        self.rules = rules_with_weights
        self.logger = logger

    def run(self, data):
        results = []
        for rule, weight in self.rules:
            score = rule.evaluate(data)
            weighted = score * weight
            self.logger.debug(f"{rule.__class__.__name__}: score={score}, weight={weight:.2f} → weighted={weighted:.2f}")
            results.append(weighted)
        return results
