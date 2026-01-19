import inspect
from core.rules.base_rule import Rule

class RuleRegistry:
    _rules = {}

    @classmethod
    def register(cls, rule_cls):
        """
        Registrierung einer Rule-Klasse
        """
        if not issubclass(rule_cls, Rule):
            raise TypeError("Only Rule subclasses can be registered")

        cls._rules[rule_cls.__name__] = rule_cls
        return rule_cls  # wichtig für Decorator

    @classmethod
    def get(cls, name: str):
        return cls._rules.get(name)

    @classmethod
    def all(cls):
        return cls._rules

    @classmethod
    def create_rules(cls, config: list, logger):
        """
        config = [
            {"name": "ValueRule", "weight": 0.5, "params": {"min_value": 60}},
            {"name": "RiskRule", "weight": 0.3, "params": {"max_risk": 0.3}},
        ]
        """
        rules = []

        for entry in config:
            rule_cls = cls.get(entry["name"])
            if not rule_cls:
                raise ValueError(f"Rule '{entry['name']}' not registered")

            params = entry.get("params", {})
            rule = rule_cls(logger=logger, **params)
            rules.append((rule, entry["weight"]))

        return rules
