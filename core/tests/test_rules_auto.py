# tests/test_rules_auto.py
import importlib
import pkgutil
import inspect
from core.rules import __path__ as rules_path
from core.rule_engine import RuleEngine
from core.decision import Decision
from evaluation.scorer import Scorer
from app_logging.logger import setup_logger

def test_all_rules():
    logger = setup_logger()

    # Dynamisch alle Klassen in core.rules laden
    rules_classes = []
    for _, modname, _ in pkgutil.iter_modules(rules_path):
        module = importlib.import_module(f"core.rules.{modname}")
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if hasattr(obj, "evaluate"):
                rules_classes.append(obj)

    # Testdaten
    test_data = [
        {"value": 70, "risk": 0.2, "volatility": 0.15},
        {"value": 50, "risk": 0.4, "volatility": 0.25},
        {"value": 60, "risk": 0.3, "volatility": 0.2},
        {"value": 40, "risk": 0.5},
        {"risk": 0.2, "volatility": 0.1},
        {"value": 65},
    ]

    # Regeln + Gewichte (alle automatisch initialisiert)
    rules = [(cls(logger), 1.0/len(rules_classes)) for cls in rules_classes]

    engine = RuleEngine(rules, logger)
    scorer = Scorer(logger)
    decision_system = Decision(logger, threshold_accept=0.5, threshold_reject=-0.5)

    # Testfälle ausführen
    for i, data in enumerate(test_data):
        scores = engine.run(data)
        total = scorer.total_score(scores)
        decision = decision_system.make(total)
        print(f"Test Case {i+1}: Data={data} | Total={total:.2f} | Decision={decision}")

if __name__ == "__main__":
    test_all_rules()
