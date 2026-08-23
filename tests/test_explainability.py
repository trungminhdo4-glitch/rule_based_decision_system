# tests/test_explainability.py

from core.explain.explainable_rule_engine import ExplainableRuleEngine
from core.decision import Decision
from evaluation.scorer import Scorer
from app_logging.logger import setup_logger

from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from core.rules.volatility_rule import VolatilityRule


def test_explainability():
    logger = setup_logger()

    rules = [
        (ValueRule(logger, min_value=60), 0.5),
        (RiskRule(logger, max_risk=0.3), 0.3),
        (VolatilityRule(logger, max_volatility=0.2), 0.2),
    ]

    engine = ExplainableRuleEngine(rules, logger)
    scorer = Scorer(logger)
    decision_system = Decision(logger)

    data = {"value": 70, "risk": 0.2, "volatility": 0.15}

    scores, explanation = engine.run(data)

    # Alle drei Regeln bestehen -> raw=+1.0, gewichtet = raw * Gewicht
    assert scores == [0.5, 0.3, 0.2], (
        f"erwartete gewichtete Scores [0.5, 0.3, 0.2], got {scores}"
    )

    # Die Erklaerung enthaelt je Regel Name, Gewichte und Grund
    summary_text = explanation.summary()
    assert isinstance(summary_text, str) and summary_text.strip(), (
        "Erklaerung darf nicht leer sein"
    )
    for rule_name in ("ValueRule", "RiskRule", "VolatilityRule"):
        assert rule_name in summary_text, f"Erklaerung muss {rule_name} nennen"
    assert "weight=0.5" in summary_text and "weight=0.3" in summary_text

    total = scorer.total_score(scores)
    assert abs(total - 1.0) < 1e-9, (
        f"Total aus gewichteten Scores muss 1.0 sein, got {total}"
    )

    decision, lines = decision_system.make(total)
    assert decision == "ACCEPT"
    assert lines == []


if __name__ == "__main__":
    test_explainability()
