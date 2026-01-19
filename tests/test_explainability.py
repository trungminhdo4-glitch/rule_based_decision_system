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
    total = scorer.total_score(scores)
    decision = decision_system.make(total)

    print("Decision:", decision)
    print("Explanation:")
    print(explanation.summary())

if __name__ == "__main__":
    test_explainability()
