class AdaptiveEngine:
    def __init__(self, rules, decision_system, logger):
        self.rules = rules
        self.decision_system = decision_system
        self.logger = logger

    # 1️⃣ Gewichte anpassen
    def adapt_weights(self, history, alpha=0.2):
        if not history.history:
            return

        rule_scores = {r.__class__.__name__: [] for r in self.rules}

        for entry in history.history:
            for d in entry["details"]:
                rule_scores[d["rule"]].append(abs(d["score"]))

        total = sum(sum(v) for v in rule_scores.values()) or 1.0

        for rule in self.rules:
            name = rule.__class__.__name__
            avg = sum(rule_scores[name]) / max(1, len(rule_scores[name]))
            old = rule.weight
            rule.weight = (1-alpha)*old + alpha*(avg/total)
            self.logger.debug(f"AdaptiveEngine | weight {name}: {old:.3f} → {rule.weight:.3f}")

    # 2️⃣ Schwellen anpassen
    def adapt_thresholds(self, history, alpha=0.05, window=5):
        if not history.history:
            return

        last = history.history[-window:]
        hold_ratio = sum(e["decision"] == "HOLD" for e in last) / len(last)

        self.decision_system.threshold_accept *= (1 - alpha * hold_ratio)
        self.decision_system.threshold_reject *= (1 + alpha * hold_ratio)

        self.decision_system.threshold_accept = min(max(self.decision_system.threshold_accept, 0.1), 0.9)
        self.decision_system.threshold_reject = min(max(self.decision_system.threshold_reject, -0.9), -0.1)

    # 3️⃣ Regelparameter anpassen
    def adapt_rule_parameters(self, history, alpha=0.05):
        from core.rules.value_rule import ValueRule
        from core.rules.risk_rule import RiskRule
        from core.rules.volatility_rule import VolatilityRule

        for rule in self.rules:
            scores = [
                d["score"]
                for entry in history.history
                for d in entry["details"]
                if d["rule"] == rule.__class__.__name__
            ]
            if not scores:
                continue

            avg = sum(scores)/len(scores)

            if isinstance(rule, ValueRule):
                rule.min_value += alpha*(1-avg)
            elif isinstance(rule, RiskRule):
                rule.max_risk = min(max(rule.max_risk + alpha*(-avg), 0), 1)
            elif isinstance(rule, VolatilityRule):
                rule.max_volatility = min(max(rule.max_volatility + alpha*(-avg), 0), 1)

