# tests/test_integration.py

from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from core.rules.volatility_rule import VolatilityRule
from core.rule_engine import RuleEngine
from core.decision import Decision
from evaluation.scorer import Scorer
from app_logging.logger import setup_logger
from data.input_data import get_sample_data

def test_integration():
    logger = setup_logger()

    # Sample Data + zusätzliche Testfälle
    data_list = get_sample_data() + [
        {"value": 70, "risk": 0.2, "volatility": 0.15},  # alles gut → ACCEPT
        {"value": 50, "risk": 0.4, "volatility": 0.25},  # schlechte Werte → REJECT
    ]

    # Regeln + Gewichte
    rules = [
        (ValueRule(logger, min_value=60), 0.5),
        (RiskRule(logger, max_risk=0.3), 0.3),
        (VolatilityRule(logger, max_volatility=0.2), 0.2)
    ]

    # RuleEngine, Scorer und Decision initialisieren
    engine = RuleEngine(rules, logger)
    scorer = Scorer(logger)
    decision_system = Decision(logger, threshold_accept=0.5, threshold_reject=-0.5)

    # End-to-End-Test
    for i, data in enumerate(data_list):
        logger.info(f"--- Test Case {i+1} ---")
        scores = engine.run(data)
        total = scorer.total_score(scores)
        decision = decision_system.make(total)
        print(f"Final Decision for Case {i+1}: {decision}")


if __name__ == "__main__":
    test_integration()

