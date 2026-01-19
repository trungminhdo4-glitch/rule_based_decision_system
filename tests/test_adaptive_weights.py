# tests/test_adaptive_weights.py
import pytest
from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from core.rules.volatility_rule import VolatilityRule
from main import calculate_adaptive_weights, HistoricalPerformance

class DummyLogger:
    def info(self, msg): pass
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

def generate_test_data():
    """Erstellt eine Reihe von Testdaten mit variierenden Scores"""
    return [
        {"value": 70, "risk": 0.2, "volatility": 0.15},  # alle gut
        {"value": 50, "risk": 0.4, "volatility": 0.25},  # alle schlecht
        {"value": 65, "risk": 0.1, "volatility": 0.18},  # mix
        {"value": 40, "risk": 0.5, "volatility": 0.3},   # alle schlecht
        {"value": 75, "risk": 0.25, "volatility": 0.1},  # alle gut
    ]

def test_adaptive_weights_increase_for_effective_rules():
    logger = DummyLogger()
    rules = [
        ValueRule(logger, min_value=60),
        RiskRule(logger, max_risk=0.3),
        VolatilityRule(logger, max_volatility=0.2)
    ]
    # Initial gleiche Gewichte
    for r in rules:
        r.weight = 1.0 / len(rules)

    history = HistoricalPerformance()
    data_list = generate_test_data()

    # Fülle Historie und berechne neue Gewichte
    for data in data_list:
        scores = [r.evaluate(data) for r in rules]
        total = sum(scores[i]*rules[i].weight for i in range(len(rules)))
        decision = "ACCEPT" if total >= 0.5 else "REJECT" if total <= -0.5 else "HOLD"
        details = [{"rule": r.__class__.__name__, "score": scores[i]} for i, r in enumerate(rules)]
        history.add(data, total, decision, details)

    # Berechne adaptive Gewichte
    new_weights = calculate_adaptive_weights(rules, history, alpha=0.2)

    # Tests:
    # 1. Alle Regeln haben ein Gewicht > 0
    assert all(w > 0 for w in new_weights.values()), "Alle Gewichte müssen positiv sein"
    # 2. Summe aller Gewichte ≈ 1
    assert abs(sum(new_weights.values()) - 1.0) < 1e-6, "Summe der Gewichte muss 1 sein"
    # 3. Effektive Regeln (ValueRule) sollten tendenziell höheres Gewicht haben
    assert new_weights["ValueRule"] >= new_weights["VolatilityRule"], "ValueRule sollte tendenziell höheres Gewicht haben"

if __name__ == "__main__":
    pytest.main([__file__])
