# core/explain/explainable_rule_engine.py

from core.explain.explanation import Explanation


class ExplainableRuleEngine:
    def __init__(self, rules, logger):
        # Tupel-Gewicht ist autoritative Initialisierung; run() liest
        # rule.weight live, damit Erklärung und Scoring übereinstimmen
        self.rules = []
        for rule, weight in rules:
            rule.weight = weight
            self.rules.append(rule)
        self.logger = logger

    def run(self, data):
        explanation = Explanation()
        weighted_scores = []

        for rule in self.rules:
            raw_score = rule.evaluate(data)
            weighted = raw_score * rule.weight
            weighted_scores.append(weighted)

            reason = getattr(rule, "last_reason", "no reason provided")

            explanation.add(
                rule_name=rule.__class__.__name__,
                raw_score=raw_score,
                weight=rule.weight,
                weighted_score=weighted,
                reason=reason,
            )

        return weighted_scores, explanation
