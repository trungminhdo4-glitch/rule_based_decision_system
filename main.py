# main.py
from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from core.rules.volatility_rule import VolatilityRule
from core.rule_engine import RuleEngine
from core.decision import Decision
from evaluation.scorer import Scorer
from evaluation.explanation import ExplanationAggregator
from evaluation.adaptive import AdaptiveEngine
from evaluation.visualization import plot_history
from app_logging.logger import setup_logger
from data.input_data import get_sample_data
from main_helpers import HistoricalPerformance

def main():
    logger = setup_logger()
    data_list = get_sample_data()

    # Regeln initialisieren
    rule_objects = [
        ValueRule(logger, min_value=60),
        RiskRule(logger, max_risk=0.3),
        VolatilityRule(logger, max_volatility=0.2)
    ]
    # Startgewicht gleichmäßig
    for r in rule_objects:
        r.weight = 1.0 / len(rule_objects)

    # Systeme initialisieren
    engine = RuleEngine([(r, r.weight) for r in rule_objects], logger)
    decision_system = Decision(logger)
    scorer = Scorer(logger)
    aggregator = ExplanationAggregator([(r, r.weight) for r in rule_objects])
    history = HistoricalPerformance()
    adaptive = AdaptiveEngine(rule_objects, decision_system, logger)

    # Durch alle Datenpunkte iterieren
    for i, data in enumerate(data_list):
        print(f"--- Data Point {i+1} ---")
        scores = engine.run(data)
        total_score = scorer.total_score(scores)

        total, details = aggregator.aggregate(data)
        aggregator.pretty_print(total, details)

        decision, explanation = decision_system.make(
            total_score, [(d["rule"], d["score"], d["weight"], d["reason"]) for d in details]
        )
        print(f"Final Decision: {decision}")
        for line in explanation:
            print("-", line)

        # Historie speichern
        history.add(
            data, total_score, decision, details,
            weights={r.__class__.__name__: r.weight for r in rule_objects},
            thresholds={"accept": decision_system.threshold_accept, "reject": decision_system.threshold_reject}
        )

        # Adaptive Updates
        adaptive.adjust_weights(history)
        adaptive.adjust_rule_parameters(history)
        adaptive.adapt_thresholds(history)

    # Zusammenfassung und Visualisierung
    summary = history.summary()
    print("=== Performance Summary ===")
    print(summary)
    plot_history(history)

if __name__ == "__main__":
    main()
