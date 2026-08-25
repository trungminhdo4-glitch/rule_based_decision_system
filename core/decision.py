import math


class Decision:
    def __init__(self, logger, threshold_accept=0.5, threshold_reject=-0.5):
        self.logger = logger
        self.threshold_accept = threshold_accept
        self.threshold_reject = threshold_reject

    def make(self, total_score, rule_details=None):
        if isinstance(total_score, float) and not math.isfinite(total_score):
            decision = "HOLD"
        elif total_score >= self.threshold_accept:
            decision = "ACCEPT"
        elif total_score <= self.threshold_reject:
            decision = "REJECT"
        else:
            decision = "HOLD"
        self.logger.info(f"Total score={total_score} → Decision: {decision}")

        explanation = []
        if rule_details:
            for rule_name, score, weight, reason in rule_details:
                explanation.append(f"{rule_name}: raw={score}, weight={weight:.2f}, weighted={score*weight:.2f} | {reason}")
        return decision, explanation



