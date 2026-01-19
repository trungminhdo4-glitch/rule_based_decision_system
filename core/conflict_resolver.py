class ConflictResolver:
    """
    Prüft auf widersprüchliche Regel-Outputs und priorisiert kritische Regeln.
    """

    def __init__(self, priority_order=None, logger=None):
        """
        priority_order: Liste der Regel-Namen nach Wichtigkeit, z.B. ['RiskRule', 'ValueRule', 'VolatilityRule']
        """
        self.priority_order = priority_order or ['RiskRule', 'ValueRule', 'VolatilityRule']
        self.logger = logger

    def resolve(self, rule_details, initial_decision):
        """
        rule_details: Liste von Dictionaries mit 'rule', 'score', 'weight', 'reason'
        initial_decision: Entscheidung vor Konfliktauflösung
        """
        conflict_info = []

        # Prüfe auf widersprüchliche Scores
        positive = [d for d in rule_details if d['score'] > 0]
        negative = [d for d in rule_details if d['score'] < 0]

        if positive and negative:
            conflict_info.append("Konflikt zwischen positiven und negativen Regeln erkannt")

            # Priorisiere kritische Regeln
            for rule_name in self.priority_order:
                for d in rule_details:
                    if d['rule'] == rule_name:
                        if d['score'] > 0:
                            decision = "ACCEPT"
                        elif d['score'] < 0:
                            decision = "REJECT"
                        else:
                            continue
                        conflict_info.append(f"{rule_name} bestimmt Entscheidung: {decision}")
                        return decision, conflict_info

        # Kein Konflikt oder keine kritischen Regeln → ursprüngliche Entscheidung behalten
        return initial_decision, conflict_info
