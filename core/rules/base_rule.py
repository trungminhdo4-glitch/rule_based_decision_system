class Rule:
    def __init__(self, logger):
        self.logger = logger
        self.last_reason = ""
        self.weight = 0.0

    def evaluate(self, data) -> float:
        raise NotImplementedError("Evaluate method not implemented")

