from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from core.rules.volatility_rule import VolatilityRule
from core.rule_engine import RuleEngine
from core.decision import Decision
from evaluation.scorer import Scorer
from app_logging.logger import setup_logger


def test_rule_decisions():
    logger = setup_logger()

    # Testdaten + erwartete Decisions
    test_cases = [
        ({"value": 70, "risk": 0.2, "volatility": 0.15}, "ACCEPT"),
        ({"value": 50, "risk": 0.4, "volatility": 0.25}, "REJECT"),
        ({"value": 60, "risk": 0.3, "volatility": 0.2}, "ACCEPT"),
        ({"value": 40, "risk": 0.5}, "REJECT"),
        ({"risk": 0.2, "volatility": 0.1}, "ACCEPT"),  # Total=0.5 -> inklusive Grenze
        ({"risk": 0.2}, "HOLD"),  # Total=0.3 -> zwischen Thresholds
        ({"value": 65}, "ACCEPT"),
    ]

    # Regeln + Gewichte
    rules = [
        (ValueRule(logger, min_value=60), 0.5),
        (RiskRule(logger, max_risk=0.3), 0.3),
        (VolatilityRule(logger, max_volatility=0.2), 0.2),
    ]

    engine = RuleEngine(rules, logger)
    scorer = Scorer(logger)
    decision_system = Decision(logger, threshold_accept=0.5, threshold_reject=-0.5)

    for i, (data, expected_decision) in enumerate(test_cases):
        scores = engine.run(data)
        total = scorer.total_score(scores)
        decision, explanation = decision_system.make(total)
        assert decision == expected_decision, (
            f"Test Case {i + 1} failed: expected {expected_decision}, got {decision}"
        )
        print(f"Test Case {i + 1} passed: Decision={decision}")


if __name__ == "__main__":
    test_rule_decisions()
