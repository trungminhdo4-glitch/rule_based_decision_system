# main_helpers.py
class HistoricalPerformance:
    """Speichert Entscheidungen, Scores, Gewichte und Thresholds"""
    def __init__(self):
        self.history = []
        self.weights_history = []
        self.thresholds_history = []

    def add(self, data_point, total_score, decision, details, weights, thresholds):
        self.history.append({
            "data": data_point,
            "total_score": total_score,
            "decision": decision,
            "details": details
        })
        self.weights_history.append(weights.copy())
        self.thresholds_history.append(thresholds.copy())

    def summary(self):
        scores = [entry["total_score"] for entry in self.history]
        return {
            "count": len(scores),
            "mean_score": sum(scores)/len(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "max_score": max(scores) if scores else 0
        }
