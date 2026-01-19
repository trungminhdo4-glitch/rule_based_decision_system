# core/rules/rule_test_cases.py

TEST_CASES_BY_RULE = {
    "ValueRule": [
        {"value": 59},
        {"value": 60},
        {"value": 80},
        {},
    ],
    "RiskRule": [
        {"risk": 0.29},
        {"risk": 0.3},
        {"risk": 0.5},
        {},
    ],
    "VolatilityRule": [
        {"volatility": 0.19},
        {"volatility": 0.2},
        {"volatility": 0.3},
        {},
    ],
}
