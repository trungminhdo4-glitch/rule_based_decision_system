# test_rules.py
import pytest

from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from app_logging.logger import setup_logger


def test_value_rule():
    logger = setup_logger()
    rule = ValueRule(logger, min_value=60)

    assert rule.evaluate({"value": 50}) == -1.0, "Value < min failed"
    assert rule.evaluate({"value": 75}) == 1.0, "Value > min failed"

    print("ValueRule tests passed")


def test_value_rule_invalid_and_missing_input():
    """Nicht-numerische Werte duerfen die Regel nicht zum Absturz bringen.

    Familienvertrag laut RiskRule/VolatilityRule: fehlender oder
    invalider Typ -> neutral 0.0 mit Grund 'value missing or invalid'.
    """
    logger = setup_logger()
    rule = ValueRule(logger, min_value=60)

    for invalid in ["100", "", [], {}]:
        result = rule.evaluate({"value": invalid})
        assert result == 0.0, (
            f"value={invalid!r} muss neutral 0.0 liefern, got {result!r}"
        )
        assert rule.last_reason == "value missing or invalid"


def test_value_rule_valid_boundaries():
    logger = setup_logger()
    rule = ValueRule(logger, min_value=60)

    assert rule.evaluate({"value": 59}) == -1.0
    assert rule.evaluate({"value": 60}) == 1.0
    assert rule.evaluate({"value": 80}) == 1.0
    assert rule.last_reason == "value=80 ≥ 60"


def test_value_rule_none_is_neutral():
    logger = setup_logger()
    rule = ValueRule(logger, min_value=60)

    assert rule.evaluate({}) == 0.0
    assert rule.evaluate({"value": None}) == 0.0


@pytest.mark.parametrize("bool_input", [True, False])
def test_value_rule_bool_is_numeric_by_family_contract(bool_input):
    """bool ist von int abgeleitet und gilt familienweit als numerisch.

    RiskRule/VolatilityRule akzeptieren bools heute ebenfalls; dieses Verhalten
    wird hier bewusst festgeschrieben, nicht zufaellig geaendert.
    """
    logger = setup_logger()
    rule = ValueRule(logger, min_value=60)

    # True == 1 < 60 -> -1.0; False == 0 < 60 -> -1.0 (bei min_value=60)
    assert rule.evaluate({"value": bool_input}) == -1.0


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
