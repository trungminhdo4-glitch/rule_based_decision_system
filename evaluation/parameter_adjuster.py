from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from core.rules.volatility_rule import VolatilityRule

def adjust_rule_parameters(rules, history, alpha=0.05):
    """Dynamische Anpassung der Regel-Parameter basierend auf Historie"""
    if not history.history:
        return

    for rule in rules:
        relevant_scores = []
        for entry in history.history:
            for d in entry["details"]:
                if d["rule"] == rule.__class__.__name__:
                    relevant_scores.append(d["score"])
        if not relevant_scores:
            continue
        avg_score = sum(relevant_scores) / len(relevant_scores)

        if isinstance(rule, ValueRule):
            delta = alpha * (1 - avg_score)
            rule.min_value += delta
        elif isinstance(rule, RiskRule):
            delta = alpha * (-avg_score)
            rule.max_risk += delta
            rule.max_risk = max(0.0, min(rule.max_risk, 1.0))
        elif isinstance(rule, VolatilityRule):
            delta = alpha * (-avg_score)
            rule.max_volatility += delta
            rule.max_volatility = max(0.0, min(rule.max_volatility, 1.0))
