class HistoricalPerformance:
    def __init__(self, storage=None):
        self.history = []
        self.storage = storage

    def add(self, data, total_score, decision, details, **meta):
        entry = {
            "data": data,
            "total_score": total_score,
            "decision": decision,
            "details": details,
            **meta
        }
        self.history.append(entry)

        if self.storage:
            self.storage.save(self.history)

    def summary(self):
        ...
class HistoryStorage:
    ...

