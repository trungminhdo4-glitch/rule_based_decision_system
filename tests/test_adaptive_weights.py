# tests/test_adaptive_weights.py
from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from core.rules.volatility_rule import VolatilityRule
from evaluation.adaptive import AdaptiveEngine
from main_helpers import HistoricalPerformance


class DummyLogger:
    def info(self, msg):
        pass

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


def build_system():
    logger = DummyLogger()
    rules = [
        ValueRule(logger, min_value=60),
        RiskRule(logger, max_risk=0.3),
        VolatilityRule(logger, max_volatility=0.2),
    ]
    # Startgewichte gleichverteilt, wie in main.py
    for r in rules:
        r.weight = 1.0 / len(rules)
    history = HistoricalPerformance()
    adaptive = AdaptiveEngine(rules, None, logger)
    return rules, history, adaptive


def feed_history(rules, history, data_list):
    """Befuellt die Historie ueber denselben Details-Pfad wie main.py."""
    for data in data_list:
        details = [
            {"rule": r.__class__.__name__, "score": r.evaluate(data)} for r in rules
        ]
        total = sum(d["score"] * r.weight for d, r in zip(details, rules))
        history.add(
            data,
            total,
            "HOLD",
            details,
            weights={r.__class__.__name__: r.weight for r in rules},
            thresholds={"accept": 0.5, "reject": -0.5},
        )


def test_adjust_weights_favours_consistently_passing_rule():
    rules, history, adaptive = build_system()

    # ValueRule besteht jeden Fall; RiskRule hat fast nur fehlende Werte
    # (Score 0); VolatilityRule ist ueberwiegend irrelevant -> niedrigster Anteil.
    data_list = [
        {"value": 70},
        {"value": 75},
        {"value": 80, "volatility": 0.3},
        {"value": 65},
    ]
    initial_weights = {r.__class__.__name__: r.weight for r in rules}
    feed_history(rules, history, data_list)

    adaptive.adjust_weights(history, alpha=0.2)

    new_weights = {r.__class__.__name__: r.weight for r in rules}

    # 1. Alle Gewichte bleiben positiv (EMA positiver Anteile)
    assert all(w > 0 for w in new_weights.values()), (
        "Alle Gewichte muessen positiv sein"
    )
    # 2. Die Gewichtssumme bleibt 1: (1-a)*sum(old) + a*sum(share) = 1
    assert abs(sum(new_weights.values()) - 1.0) < 1e-9, (
        "Summe der Gewichte muss 1 bleiben"
    )
    # 3. Die konsistent bestehende Regel erhaelt das meiste Gewicht
    assert new_weights["ValueRule"] > new_weights["VolatilityRule"], (
        "ValueRule sollte mehr Gewicht erhalten als die weitgehend inaktive VolatilityRule"
    )
    # 4. adaptation fand tatsaechlich statt
    assert new_weights != initial_weights, (
        "Gewichte muessen sich durch die Historie veraendern"
    )


if __name__ == "__main__":
    test_adjust_weights_favours_consistently_passing_rule()
