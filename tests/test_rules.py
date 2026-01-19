# test_rules.py
from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from app_logging.logger import setup_logger

def test_value_rule():
    logger = setup_logger()
    rule = ValueRule(logger, min_value=60)

    assert rule.evaluate({"value": 50}) == -1.0, "Value < min failed"
    assert rule.evaluate({"value": 75}) == 1.0, "Value > min failed"

    print("ValueRule tests passed")

def test_risk_rule():
    logger = setup_logger()
    rule = RiskRule(logger, max_risk=0.3)

    assert rule.evaluate({"risk": 0.5}) == -1.0, "Risk too high failed"
    assert rule.evaluate({"risk": 0.2}) == 1.0, "Risk low failed"
    assert rule.evaluate({}) == 0.0, "Risk missing failed"

    print("RiskRule tests passed")

if __name__ == "__main__":
    test_value_rule()
    test_risk_rule()
