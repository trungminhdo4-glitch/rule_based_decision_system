# core/rule.py
from abc import ABC, abstractmethod

class Rule(ABC):
    @abstractmethod
    def evaluate(self, data) -> float:
        """
        Gibt einen Score zurück:
        positiv = gut
        negativ = schlecht
        """
        pass
