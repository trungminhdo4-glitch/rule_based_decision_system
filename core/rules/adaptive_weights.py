class AdaptiveWeights:
    def __init__(self, rules, lr=0.1, trend_lr=0.05, max_change=0.05):
        self.rules = rules
        self.lr = lr
        self.trend_lr = trend_lr
        self.max_change = max_change

    def update(self, history):
        if not history.history:
            return

        for i, rule in enumerate(self.rules):
            scores = [
                entry["details"][i]["score"]
                for entry in history.history
                if len(entry["details"]) > i
            ]
            if len(scores) < 2:
                continue

            avg = sum(scores)/len(scores)
            trend = scores[-1] - scores[0]

            adjustment = avg*self.lr + max(-self.max_change, min(self.max_change, trend*self.trend_lr))
            rule.weight = min(max(rule.weight + adjustment, 0), 1)
