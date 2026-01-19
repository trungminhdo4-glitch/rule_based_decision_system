# evaluation/adaptive.py
class AdaptiveEngine:
    def __init__(self, rules, decision_system, logger):
        self.rules = rules
        self.decision_system = decision_system
        self.logger = logger

    def adjust_weights(self, history, alpha=0.2):
        """EMA-basierte Gewichtsanpassung"""
        if not history.history:
            return
        rule_scores = {rule.__class__.__name__: [] for rule in self.rules}
        for entry in history.history:
            for d in entry["details"]:
                rule_scores[d["rule"]].append(abs(d["score"]))
        avg_scores = {r: sum(scores)/len(scores) if scores else 0.0 for r, scores in rule_scores.items()}
        total = sum(avg_scores.values()) or 1.0
        for rule in self.rules:
            name = rule.__class__.__name__
            old_weight = getattr(rule, "weight", 1.0/len(self.rules))
            new_weight = (1-alpha)*old_weight + alpha*(avg_scores[name]/total)
            rule.weight = new_weight
            self.logger.debug(f"AdaptiveEngine: Updated weight {name} -> {new_weight:.3f}")

    def adjust_rule_parameters(self, history, alpha=0.05):
        """Dynamische Anpassung der Regelparameter"""
        if not history.history:
            return
        for rule in self.rules:
            relevant_scores = [d["score"] for entry in history.history
                               for d in entry["details"]
                               if d["rule"] == rule.__class__.__name__]
            if not relevant_scores:
                continue
            avg_score = sum(relevant_scores)/len(relevant_scores)
            if hasattr(rule, "min_value"):
                rule.min_value += alpha*(1-avg_score)
            if hasattr(rule, "max_risk"):
                rule.max_risk = max(0.0, min(rule.max_risk + alpha*(-avg_score), 1.0))
            if hasattr(rule, "max_volatility"):
                rule.max_volatility = max(0.0, min(rule.max_volatility + alpha*(-avg_score), 1.0))

    def adapt_thresholds(self, history, alpha_thresh=0.05, window=5):
        """Adaptive Thresholds anhand der letzten N Entscheidungen"""
        if not history.history:
            return
        last_entries = history.history[-window:]
        hold_ratio = sum(e["decision"]=="HOLD" for e in last_entries)/max(1,len(last_entries))
        self.decision_system.threshold_accept *= (1-alpha_thresh*hold_ratio)
        self.decision_system.threshold_reject *= (1+alpha_thresh*hold_ratio)
        self.decision_system.threshold_accept = min(max(self.decision_system.threshold_accept, 0.1), 0.9)
        self.decision_system.threshold_reject = min(max(self.decision_system.threshold_reject, -0.9), -0.1)

