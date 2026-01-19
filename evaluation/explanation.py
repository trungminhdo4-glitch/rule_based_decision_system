class ExplanationAggregator:
    def __init__(self, rules_with_weights):
        self.rules_with_weights = rules_with_weights

    def aggregate(self, data):
        details = []
        total = 0.0
        for rule, weight in self.rules_with_weights:
            score = rule.evaluate(data)
            total += score * weight
            details.append({
                "rule": rule.__class__.__name__,
                "score": score,
                "weight": weight,
                "reason": rule.last_reason
            })
        return total, details

    def pretty_print(self, total, details):
        print(f"Total Score={total:.2f}")
        for d in details:
            print(f"- {d['rule']}: raw={d['score']}, weight={d['weight']:.2f}, weighted={d['score']*d['weight']:.2f} | {d['reason']}")
