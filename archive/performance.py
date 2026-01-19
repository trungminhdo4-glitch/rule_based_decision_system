import statistics
from evaluation.history import HistoryStorage

class HistoricalPerformance:
    def __init__(self, storage: HistoryStorage = None):
        self.history = []
        self.storage = storage
        if storage:
            self.history = storage.load()

    def add(self, data_point, total_score, decision, details):
        self.history.append({
            "data": data_point,
            "total_score": total_score,
            "decision": decision,
            "details": details
        })
        if self.storage:
            self.storage.save(self.history)

    def summary(self):
        if not self.history:
            return {}
        scores = [entry["total_score"] for entry in self.history]
        return {
            "count": len(scores),
            "mean_score": statistics.mean(scores),
            "min_score": min(scores),
            "max_score": max(scores)
        }
