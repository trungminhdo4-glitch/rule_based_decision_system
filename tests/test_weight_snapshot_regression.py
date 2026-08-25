# tests/test_weight_snapshot_regression.py
# Regressionstests: angewandte Gewichte == rule.weight == aufgezeichnete Gewichte
from core.rules.value_rule import ValueRule
from core.rules.risk_rule import RiskRule
from core.rules.volatility_rule import VolatilityRule
from core.rule_engine import RuleEngine
from evaluation.explanation import ExplanationAggregator
from evaluation.adaptive import AdaptiveEngine
from main_helpers import HistoricalPerformance
from core.explain.explainable_rule_engine import ExplainableRuleEngine


class DummyLogger:
    def info(self, msg):
        pass

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


def _build_rules():
    logger = DummyLogger()
    return logger, [
        ValueRule(logger, min_value=60),
        RiskRule(logger, max_risk=0.3),
        VolatilityRule(logger, max_volatility=0.2),
    ]


def test_static_tuple_construction_unchanged():
    # I3-Anker: statische Nutzung mit Tupel-Gewichten bleibt identisch,
    # auch wenn rule.weight nie manuell gesetzt wurde (Konstruktor synchronisiert)
    logger, rules = _build_rules()
    rules_with_weights = [(rules[0], 0.5), (rules[1], 0.3), (rules[2], 0.2)]
    engine = RuleEngine(rules_with_weights, logger)

    data = {"value": 70, "risk": 0.2, "volatility": 0.15}
    scores = engine.run(data)
    expected = 1.0 * 0.5 + 1.0 * 0.3 + 1.0 * 0.2
    assert abs(sum(scores) - expected) < 1e-12

    # dokumentierte Nebeneigenschaft: Tupel-Gewicht wird auf rule.weight gespiegelt
    assert all(r.weight == w for r, (_, w) in zip(rules, rules_with_weights))


def test_engine_and_aggregator_use_live_weights_after_adaptation():
    # I5: nach adjust_weights muessen naechste Evaluationen die neuen Gewichte nutzen
    logger, rules = _build_rules()
    for r in rules:
        r.weight = 1.0 / len(rules)

    engine = RuleEngine([(r, r.weight) for r in rules], logger)
    aggregator = ExplanationAggregator([(r, r.weight) for r in rules])
    adaptive = AdaptiveEngine(rules, None, logger)

    history = HistoricalPerformance()
    for i in range(5):
        dp = (
            {"value": 70, "risk": 0.2}
            if i < 4
            else {"value": 70, "risk": 0.2, "volatility": 0.15}
        )
        total, details = aggregator.aggregate(dp)
        history.add(
            dp,
            total,
            "ACCEPT",
            details,
            weights={r.__class__.__name__: r.weight for r in rules},
            thresholds={"accept": 0.5, "reject": -0.5},
        )
        adaptive.adjust_weights(history)

    live_weights = {r.__class__.__name__: r.weight for r in rules}
    assert len(set(round(w, 9) for w in live_weights.values())) > 1, (
        "Testaufbau: Adaptation muss divergente Gewichte erzeugen"
    )

    data = {"value": 70, "risk": 0.2}
    scores = engine.run(data)
    _, details = aggregator.aggregate(data)

    for d in details:
        assert abs(d["weight"] - live_weights[d["rule"]]) < 1e-12, (
            f"{d['rule']}: Pipeline nutzt {d['weight']}, rule.weight ist "
            f"{live_weights[d['rule']]} - Stale Snapshot"
        )
    expected_total = sum(r.evaluate(data) * r.weight for r in rules)
    assert abs(sum(scores) - expected_total) < 1e-12


def test_recorded_weights_match_applied_weights():
    # I5: was in die Historie geschrieben wird, muss den angewandten Gewichten entsprechen
    logger, rules = _build_rules()
    for r in rules:
        r.weight = 1.0 / len(rules)

    engine = RuleEngine([(r, r.weight) for r in rules], logger)
    aggregator = ExplanationAggregator([(r, r.weight) for r in rules])
    adaptive = AdaptiveEngine(rules, None, logger)
    history = HistoricalPerformance()

    for i in range(4):
        dp = (
            {"value": 70, "risk": 0.2}
            if i < 3
            else {"value": 70, "risk": 0.2, "volatility": 0.15}
        )
        scores = engine.run(dp)
        total, details = aggregator.aggregate(dp)
        applied = {d["rule"]: d["weight"] for d in details}
        recorded = {r.__class__.__name__: r.weight for r in rules}
        assert applied == recorded or all(
            abs(applied[k] - recorded[k]) < 1e-12 for k in applied
        ), f"Historie luegt: aufgezeichnet {recorded}, angewandt {applied}"
        history.add(
            dp,
            sum(scores),
            "ACCEPT",
            details,
            weights=recorded,
            thresholds={"accept": 0.5, "reject": -0.5},
        )
        adaptive.adjust_weights(history)


def test_production_records_snapshots_before_adapting(monkeypatch):
    import main as production

    histories = []
    thresholds_used = []

    class CapturingHistory(HistoricalPerformance):
        def __init__(self):
            super().__init__()
            histories.append(self)

    class CapturingDecision(production.Decision):
        def make(self, total_score, rule_details=None):
            thresholds_used.append(
                {"accept": self.threshold_accept, "reject": self.threshold_reject}
            )
            return super().make(total_score, rule_details)

    monkeypatch.setattr(production, "setup_logger", DummyLogger)
    monkeypatch.setattr(
        production,
        "get_sample_data",
        lambda: [{}, {"value": 70}, {"value": 70}],
    )
    monkeypatch.setattr(production, "HistoricalPerformance", CapturingHistory)
    monkeypatch.setattr(production, "Decision", CapturingDecision)
    monkeypatch.setattr(production, "plot_history", lambda history: None)

    production.main()

    history = histories[0]
    assert len(history.history) == len(thresholds_used) == 3
    for entry, recorded_weights, recorded_thresholds, used_thresholds in zip(
        history.history,
        history.weights_history,
        history.thresholds_history,
        thresholds_used,
    ):
        applied_weights = {detail["rule"]: detail["weight"] for detail in entry["details"]}
        assert recorded_weights == applied_weights
        assert recorded_thresholds == used_thresholds

    # Neutral history preserves weights, but its HOLD still adapts the next thresholds.
    assert history.weights_history[1] == history.weights_history[0]
    assert history.weights_history[2] != history.weights_history[1]
    assert thresholds_used[1] != thresholds_used[0]


def test_explainable_rule_engine_uses_live_weights():
    # A4-Verifikation: ExplainableRuleEngine hat dasselbe Muster und folgt demselben Fix
    logger, rules = _build_rules()
    for r in rules:
        r.weight = 1.0 / len(rules)

    engine = ExplainableRuleEngine([(r, r.weight) for r in rules], logger)
    adaptive = AdaptiveEngine(rules, None, logger)

    history = HistoricalPerformance()
    dp = {"value": 70, "risk": 0.2}
    for i in range(6):
        scores, explanation = engine.run(
            dp if i % 2 else {"value": 70, "risk": 0.2, "volatility": 0.15}
        )
        details = [
            {
                "rule": e["rule"],
                "score": e["raw_score"],
                "weight": e["weight"],
                "reason": e["reason"],
            }
            for e in explanation.entries
        ]
        history.add(
            {"value": 70, "risk": 0.2},
            sum(scores),
            "ACCEPT",
            details,
            weights={r.__class__.__name__: r.weight for r in rules},
            thresholds={"accept": 0.5, "reject": -0.5},
        )
        adaptive.adjust_weights(history)

    live_weights = {r.__class__.__name__: round(r.weight, 9) for r in rules}
    _, explanation = engine.run(dp)
    for e in explanation.entries:
        assert abs(e["weight"] - live_weights[e["rule"]]) < 1e-9
