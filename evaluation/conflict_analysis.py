# evaluation/explanation_conflict.py

class ExplanationAggregatorWithConflict:
    def __init__(self, rules_with_weights):
        """
        rules_with_weights: List[Tuple[RuleObj, weight]]
        """
        self.rules_with_weights = rules_with_weights

    def aggregate(self, data):
        """
        Aggregiert Scores, Gründe und erkennt Konflikte.
        Returns: total_score, list_of_details, conflict_detected
        """
        total = 0.0
        details = []
        conflict_detected = False
        signs = []

        for rule, weight in self.rules_with_weights:
            score = rule.evaluate(data)
            weighted = score * weight
            reason = getattr(rule, "last_reason", "no reason provided")
            details.append({
                "rule": rule.__class__.__name__,
                "raw": score,
                "weight": weight,
                "weighted": weighted,
                "reason": reason
            })

            total += weighted
            if score != 0:
                signs.append(score > 0)

        if len(set(signs)) > 1:
            conflict_detected = True

        return total, details, conflict_detected

    def pretty_print(self, total, details, conflict_detected=False):
        print(f"Aggregated Score: {total:.2f}")
        if conflict_detected:
            print("[WARNING] Conflicting rule signals detected!")

        for d in details:
            print(
                f"- {d['rule']} → raw={d['raw']}, weight={d['weight']}, "
                f"weighted={d['weighted']:.2f} | reason: {d['reason']}"
            )
