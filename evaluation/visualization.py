# evaluation/visualization.py
import matplotlib.pyplot as plt

def plot_history(history):
    """Visualisiert Gewichte, Thresholds und Scoreverlauf"""
    if not history.history:
        return

    # Gewichte
    plt.figure(figsize=(10,5))
    for rule_name in history.weights_history[0].keys():
        plt.plot([w[rule_name] for w in history.weights_history], label=rule_name)
    plt.title("Gewichtsverlauf der Regeln")
    plt.xlabel("Data Point")
    plt.ylabel("Weight")
    plt.legend()
    plt.show()

    # Thresholds
    plt.figure(figsize=(10,5))
    plt.plot([t["accept"] for t in history.thresholds_history], label="Accept Threshold")
    plt.plot([t["reject"] for t in history.thresholds_history], label="Reject Threshold")
    plt.title("Threshold Verlauf")
    plt.xlabel("Data Point")
    plt.ylabel("Threshold")
    plt.legend()
    plt.show()

    # Total Score Verlauf
    plt.figure(figsize=(10,5))
    scores = [entry["total_score"] for entry in history.history]
    plt.plot(scores, marker='o', label="Total Score")
    plt.title("Total Score Verlauf")
    plt.xlabel("Data Point")
    plt.ylabel("Score")
    plt.grid(True)
    plt.legend()
    plt.show()

