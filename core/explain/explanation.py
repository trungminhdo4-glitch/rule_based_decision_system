# core/explain/explanation.py

class Explanation:
    def __init__(self):
        self.entries = []

    def add(self, rule_name, raw_score, weight, weighted_score, reason):
        self.entries.append({
            "rule": rule_name,
            "raw_score": raw_score,
            "weight": weight,
            "weighted_score": weighted_score,
            "reason": reason
        })

    def summary(self):
        lines = []
        for e in self.entries:
            lines.append(
                f"- {e['rule']} → "
                f"raw={e['raw_score']}, "
                f"weight={e['weight']}, "
                f"weighted={e['weighted_score']:.2f} | "
                f"{e['reason']}"
            )
        return "\n".join(lines)
