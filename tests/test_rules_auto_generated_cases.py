# tests/test_rules_auto_generated_cases.py

import inspect
from core.rules.rule_test_cases import TEST_CASES_BY_RULE
from core.rule_engine import RuleEngine
from core.decision import Decision
from evaluation.scorer import Scorer
from app_logging.logger import setup_logger

from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from core.rules.volatility_rule import VolatilityRule

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
        kwargs = {}

        for param in list(sig.parameters.values())[1:]:
            if param.name == "logger":
                kwargs["logger"] = logger
            elif param.name == "min_value":
                kwargs["min_value"] = 60
            elif param.name == "max_risk":
                kwargs["max_risk"] = 0.3
            elif param.name == "max_volatility":
                kwargs["max_volatility"] = 0.2

        rules.append((cls(**kwargs), 1.0 / len(rule_classes)))

    engine = RuleEngine(rules, logger)
    scorer = Scorer(logger)
    decision_system = Decision(logger)

    # 🔁 Alle Testfälle aus allen Rules kombinieren
    all_test_cases = []
    for cases in TEST_CASES_BY_RULE.values():
        all_test_cases.extend(cases)

    for i, data in enumerate(all_test_cases):
        scores = engine.run(data)
        total = scorer.total_score(scores)
        decision = decision_system.make(total)

        print(f"Case {i+1}: data={data} → score={total:.2f} → {decision}")

if __name__ == "__main__":
    test_rules_with_generated_cases()
