# tests/test_rules_auto_assert.py

import importlib
import pkgutil
import inspect
from core.rules import __path__ as rules_path
from core.rule_engine import RuleEngine
from core.decision import Decision
from evaluation.scorer import Scorer
from app_logging.logger import setup_logger

def test_all_rules_auto():
    logger = setup_logger()

    # --- 1. Dynamisch alle Klassen in core.rules laden ---
    rules_classes = []
    for _, modname, _ in pkgutil.iter_modules(rules_path):
        module = importlib.import_module(f"core.rules.{modname}")
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Nur Klassen, die evaluate implementieren
            if hasattr(obj, "evaluate") and not bool(getattr(obj, "__abstractmethods__", False)):
                rules_classes.append(obj)

    if not rules_classes:
        print("Keine konkreten Rule-Klassen gefunden!")
        return

    # --- 2. Testdaten ---
    test_data = [
        {"value": 70, "risk": 0.2, "volatility": 0.15},
        {"value": 50, "risk": 0.4, "volatility": 0.25},
        {"value": 60, "risk": 0.3, "volatility": 0.2},
        {"value": 40, "risk": 0.5},
        {"risk": 0.2, "volatility": 0.1},
        {"value": 65},
    ]

    # --- 3. Regeln instanziieren mit nur existierenden Parametern ---
    rules = []
    for cls in rules_classes:
        sig = inspect.signature(cls.__init__)
        kwargs = {}

        for param in list(sig.parameters.values())[1:]:  # skip 'self'
            if param.name == "logger":
                kwargs["logger"] = logger
            elif param.name == "min_value":
                kwargs["min_value"] = 60
            elif param.name == "max_risk":
                kwargs["max_risk"] = 0.3
            elif param.name == "max_volatility":
                kwargs["max_volatility"] = 0.2
            # weitere Defaults hier ergänzen

        rules.append((cls(**kwargs), 1.0 / len(rules_classes)))

    # --- 4. Engine, Scorer, Decision ---
    engine = RuleEngine(rules, logger)
    scorer = Scorer(logger)
    decision_system = Decision(logger, threshold_accept=0.5, threshold_reject=-0.5)

    # --- 5. Testfälle ausführen ---
    for i, data in enumerate(test_data):
        scores = engine.run(data)
        total = scorer.total_score(scores)
        decision = decision_system.make(total)

        # Dynamische erwartete Decision basierend auf Thresholds
        expected_decision = (
            "ACCEPT" if total >= decision_system.threshold_accept else
            "REJECT" if total <= decision_system.threshold_reject else
            "HOLD"
        )

        assert decision == expected_decision, (
            f"Test Case {i+1} failed: Total={total:.2f}, expected {expected_decision}, got {decision}"
        )
        print(f"Test Case {i+1} passed: Total={total:.2f}, Decision={decision}")

if __name__ == "__main__":
    test_all_rules_auto()
