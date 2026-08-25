class HistoricalPerformance:
    def __init__(self, storage=None):
        self.storage = storage
        self.history = storage.load() if storage is not None else []
        if not isinstance(self.history, list):
            raise TypeError("storage.load() must return a list")

    def add(self, data, total_score, decision, details, **meta):
        entry = {
            "data": data,
            "total_score": total_score,
            "decision": decision,
            "details": details,
            **meta
        }
        self.history.append(entry)

        if self.storage is not None:
            self.storage.save(self.history)

    def summary(self):
        ...
class HistoryStorage:
    ...

