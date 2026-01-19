# core/system_setup.py
from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from core.rules.volatility_rule import VolatilityRule
from core.rule_engine import RuleEngine
from core.decision import Decision
from evaluation.scorer import Scorer
from evaluation.explanation import ExplanationAggregator
from evaluation.history import HistoricalPerformance

def setup_system(logger):
    # Regeln initial
    rule_objects = [
        ValueRule(logger, min_value=60),
        RiskRule(logger, max_risk=0.3),
        VolatilityRule(logger, max_volatility=0.2)
    ]
    initial_weight = 1.0 / len(rule_objects)
    rules_with_weights = [(rule, initial_weight) for rule in rule_objects]
    for rule, weight in rules_with_weights:
        rule.weight = weight

    engine = RuleEngine(rules_with_weights, logger)
    scorer = Scorer(logger)
    decision_system = Decision(logger, threshold_accept=0.5, threshold_reject=-0.5)
    aggregator = ExplanationAggregator(rules_with_weights)
    history = HistoricalPerformance()

    return rule_objects, engine, scorer, decision_system, aggregator, history
