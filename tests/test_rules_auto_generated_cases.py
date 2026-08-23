# tests/test_rules_auto_generated_cases.py

import inspect

from tests.rule_test_cases import TEST_CASES_BY_RULE
from core.rule_engine import RuleEngine
from core.decision import Decision
from evaluation.scorer import Scorer
from app_logging.logger import setup_logger

from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from core.rules.volatility_rule import VolatilityRule


def _build_kwargs(sig_params, logger):
    kwargs = {}
    for param in sig_params:
        if param == "logger":
            kwargs["logger"] = logger
        elif param == "min_value":
            kwargs["min_value"] = 60
        elif param == "max_risk":
            kwargs["max_risk"] = 0.3
        elif param == "max_volatility":
            kwargs["max_volatility"] = 0.2
    return kwargs


def test_rules_with_generated_cases():
    logger = setup_logger()

    rule_classes = {
        "ValueRule": ValueRule,
        "RiskRule": RiskRule,
        "VolatilityRule": VolatilityRule,
    }

    rules = []
    for name, cls in rule_classes.items():
        sig = inspect.signature(cls.__init__)
        params = list(sig.parameters.values())[1:]  # skip 'self'
        rules.append(
            (
                cls(**_build_kwargs([p.name for p in params], logger)),
                1.0 / len(rule_classes),
            )
        )

    engine = RuleEngine(rules, logger)
    scorer = Scorer(logger)
    decision_system = Decision(logger)

    # Alle Testfaelle aus allen Rules kombinieren
    all_test_cases = []
    for cases in TEST_CASES_BY_RULE.values():
        all_test_cases.extend(cases)
    assert len(all_test_cases) >= len(TEST_CASES_BY_RULE), (
        "Testfall-Datei muss Faelle je Regel enthalten"
    )

    for i, data in enumerate(all_test_cases):
        scores = engine.run(data)
        total = scorer.total_score(scores)
        decision, explanation = decision_system.make(total)

        # Die Entscheidung muss konsistent zu den Thresholds sein
        expected_decision = (
            "ACCEPT"
            if total >= decision_system.threshold_accept
            else "REJECT"
            if total <= decision_system.threshold_reject
            else "HOLD"
        )
        assert decision == expected_decision, (
            f"Case {i + 1}: data={data} score={total:.2f} -> {decision}, erwartet {expected_decision}"
        )
