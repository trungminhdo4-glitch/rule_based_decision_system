import statistics

class TrendAdaptiveWeights:
    """
    Passt die Regelgewichte basierend auf Score-Trends über die Historie an.
    """
    def __init__(self, rules, learning_rate=0.05, max_change=0.05):
        self.rules = rules
        self.learning_rate = learning_rate
        self.max_change = max_change  # maximale Anpassung pro Zyklus

    def update(self, history):
        if not history:
            return

        for i, rule in enumerate(self.rules):
            # Scores der letzten n Einträge für diese Regel
            rule_scores = [
                entry["details"][i]["score"]
                for entry in history
                if len(entry["details"]) > i
            ]
            if len(rule_scores) < 2:
                continue

            # Trend = letzte - erste Score
            trend = rule_scores[-1] - rule_scores[0]

            # Anpassung proportional zum Trend, begrenzt durch max_change
            adjustment = max(-self.max_change, min(self.max_change, trend * self.learning_rate))
            new_weight = getattr(rule, "weight", 1.0/len(self.rules)) + adjustment
            new_weight = max(0.0, min(1.0, new_weight))
            rule.weight = new_weight
