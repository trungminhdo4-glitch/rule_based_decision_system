# core/explain/explainable_rule_engine.py

from core.explain.explanation import Explanation

class ExplainableRuleEngine:
    def __init__(self, rules, logger):
        self.rules = rules
        self.logger = logger

    def run(self, data):
        explanation = Explanation()
        weighted_scores = []

        for rule, weight in self.rules:
            raw_score = rule.evaluate(data)
            weighted = raw_score * weight
            weighted_scores.append(weighted)

            reason = getattr(rule, "last_reason", "no reason provided")

            explanation.add(
                rule_name=rule.__class__.__name__,
                raw_score=raw_score,
                weight=weight,
                weighted_score=weighted,
                reason=reason
            )

        return weighted_scores, explanation
