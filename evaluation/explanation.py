class ExplanationAggregator:
    def __init__(self, rules_with_weights):
        # Tupel-Gewicht ist autoritative Initialisierung; aggregate() liest
        # rule.weight live, damit Erklärungen die angewandten Gewichte zeigen
        self.rules = []
        for rule, weight in rules_with_weights:
            rule.weight = weight
            self.rules.append(rule)

    def aggregate(self, data):
        details = []
        total = 0.0
        for rule in self.rules:
            score = rule.evaluate(data)
            total += score * rule.weight
            details.append(
                {
                    "rule": rule.__class__.__name__,
                    "score": score,
                    "weight": rule.weight,
                    "reason": rule.last_reason,
                }
            )
        return total, details

    def pretty_print(self, total, details):
        print(f"Total Score={total:.2f}")
        for d in details:
            print(
                f"- {d['rule']}: raw={d['score']}, weight={d['weight']:.2f}, weighted={d['score'] * d['weight']:.2f} | {d['reason']}"
            )
