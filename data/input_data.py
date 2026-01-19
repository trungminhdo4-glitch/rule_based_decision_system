def get_sample_data():
    """
    Liefert eine Liste von Dictionaries als Testdaten für das Decision-System
    """
    return [
        {"value": 50, "risk": 0.5},   # Value zu niedrig, Risk zu hoch
        {"value": 75, "risk": 0.2},   # Value hoch, Risk niedrig
        {"value": 65, "risk": 0.1},   # beide gut
        {"value": 40},                 # Risk fehlt
        {"risk": 0.4},                 # Value fehlt
        {"value": 80, "risk": 0.3},   # perfekt
    ]
    