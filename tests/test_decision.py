from core.decision import Decision
from app_logging.logger import setup_logger

def test_decision():
    logger = setup_logger()
    
    # Thresholds: Accept >= 0.5, Reject <= -0.5
    decision_system = Decision(logger, threshold_accept=0.5, threshold_reject=-0.5)

    # Testfälle: weighted total_score → expected decision
    test_cases = [
        (0.7, "ACCEPT"),   # über Accept-Threshold
        (0.5, "ACCEPT"),   # genau Accept-Threshold
        (0.0, "HOLD"),     # zwischen Thresholds
        (-0.4, "HOLD"),    # zwischen Thresholds
        (-0.5, "REJECT"),  # genau Reject-Threshold
        (-0.7, "REJECT"),  # unter Reject-Threshold
    ]

    for total, expected in test_cases:
        result = decision_system.make(total)
        assert result == expected, f"Expected {expected}, got {result} for total_score={total}"

    print("All Decision tests passed!")

if __name__ == "__main__":
    test_decision()
