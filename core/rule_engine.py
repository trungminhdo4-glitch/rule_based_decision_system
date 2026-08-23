class RuleEngine:
    def __init__(self, rules_with_weights, logger):
        # Tupel-Gewicht ist autoritative Initialisierung; zur Laufzeit gilt
        # ausschliesslich rule.weight, damit adaptive Updates wirken
        self.rules = []
        for rule, weight in rules_with_weights:
            rule.weight = weight
            self.rules.append(rule)
        self.logger = logger

    def run(self, data):
        results = []
        for rule in self.rules:
            score = rule.evaluate(data)
            weighted = score * rule.weight
            self.logger.debug(
                f"{rule.__class__.__name__}: score={score}, weight={rule.weight:.2f} → weighted={weighted:.2f}"
            )
            results.append(weighted)
        return results
