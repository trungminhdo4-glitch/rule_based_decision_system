# tests/auto_optimize_weights.py
from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from core.rules.volatility_rule import VolatilityRule
from core.rule_engine import RuleEngine
from evaluation.scorer import Scorer
from app_logging.logger import setup_logger
from data.input_data import get_sample_data

def auto_optimize_weights():
    logger = setup_logger()
    data_list = get_sample_data()

    # Regeln initial mit gleichen Gewichten
    rules_with_weights = [
        (ValueRule(logger, min_value=60), 1.0),
        (RiskRule(logger, max_risk=0.3), 1.0),
        (VolatilityRule(logger, max_volatility=0.2), 1.0)
    ]

    # Teste jede Regel einzeln auf allen Datenpunkten
    performance = {}
    for rule, _ in rules_with_weights:
        scores = []
        for data in data_list:
            score = rule.evaluate(data)
            scores.append(score)
        mean_score = sum(scores) / len(scores)
        performance[rule.__class__.__name__] = mean_score

    # Normalisiere Scores, um Gesamtgewicht=1 zu erhalten
    total_mean = sum(abs(v) for v in performance.values())
    optimized_weights = {k: abs(v)/total_mean for k, v in performance.items()}

    print("=== Optimized Initial Weights Recommendation ===")
    for rule, weight in optimized_weights.items():
        print(f"{rule}: {weight:.2f}")

if __name__ == "__main__":
    auto_optimize_weights()
