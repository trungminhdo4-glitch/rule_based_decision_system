# tests/test_decision.py
from decimal import Decimal

import pytest

from core.decision import Decision
from app_logging.logger import setup_logger


def _make_decision_system(logger):
    return Decision(logger, threshold_accept=0.5, threshold_reject=-0.5)


def test_decision():
    logger = setup_logger()
    decision_system = _make_decision_system(logger)

    # Testfaelle: weighted total_score -> expected decision
    # Grenzen sind inklusiv: ACCEPT bei >= 0.5, REJECT bei <= -0.5
    test_cases = [
        (0.7, "ACCEPT"),  # ueber Accept-Threshold
        (0.5, "ACCEPT"),  # genau Accept-Threshold
        (0.0, "HOLD"),  # zwischen Thresholds
        (-0.4, "HOLD"),  # zwischen Thresholds
        (-0.5, "REJECT"),  # genau Reject-Threshold
        (-0.7, "REJECT"),  # unter Reject-Threshold
    ]

    for total, expected in test_cases:
        result = decision_system.make(total)
        assert isinstance(result, tuple) and len(result) == 2, (
            f"make() muss (decision, explanation) liefern, got {result!r}"
        )
        decision, explanation = result
        assert decision == expected, (
            f"Expected {expected}, got {decision} for total_score={total}"
        )
        assert explanation == [], (
            "ohne rule_details darf keine Erklaerungszeile entstehen"
        )


def test_decision_explanation_contract():
    logger = setup_logger()
    decision_system = _make_decision_system(logger)

    details = [("ValueRule", 1.0, 0.5, "value=70 >= 60")]
    decision, explanation = decision_system.make(1.0, details)

    assert decision == "ACCEPT"
    assert len(explanation) == len(details)
    assert "ValueRule" in explanation[0]
    assert "weight=0.50" in explanation[0]


@pytest.mark.parametrize(
    "total_score",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
        Decimal("NaN"),
        Decimal("Infinity"),
        Decimal("-Infinity"),
    ],
)
def test_non_finite_total_score_is_hold(total_score):
    logger = setup_logger()
    decision_system = _make_decision_system(logger)

    decision, explanation = decision_system.make(total_score)

    assert decision == "HOLD"
    assert explanation == []


@pytest.mark.parametrize(
    ("total_score", "expected"),
    [
        (Decimal("0.7"), "ACCEPT"),
        (Decimal("0"), "HOLD"),
        (Decimal("-0.7"), "REJECT"),
        (Decimal("1E+999999"), "ACCEPT"),
        (Decimal("-1E+999999"), "REJECT"),
        (10**1000, "ACCEPT"),
        (-(10**1000), "REJECT"),
    ],
)
def test_finite_numeric_total_score_retains_decision_behavior(total_score, expected):
    logger = setup_logger()
    decision_system = _make_decision_system(logger)

    decision, explanation = decision_system.make(total_score)

    assert decision == expected
    assert explanation == []


@pytest.mark.parametrize("total_score", [None, "0.7", 1 + 0j])
def test_unsupported_total_score_still_raises_type_error(total_score):
    logger = setup_logger()
    decision_system = _make_decision_system(logger)

    with pytest.raises(TypeError):
        decision_system.make(total_score)
