class Scorer:
    def __init__(self, logger):
        self.logger = logger

    def total_score(self, scores):
        total = sum(scores)
        self.logger.debug(f"Total score calculated: {total}")
        return total

