from unittest.mock import Mock

import pytest

from evaluation.history import HistoricalPerformance


def test_restores_history_from_storage():
    stored_history = [{"total_score": 0.75, "decision": "ACCEPT"}]
    storage = Mock()
    storage.load.return_value = stored_history

    history = HistoricalPerformance(storage)

    assert history.history == stored_history
    storage.load.assert_called_once_with()
    storage.save.assert_not_called()


def test_add_appends_to_restored_history_and_saves_all_entries():
    existing_entry = {"total_score": -0.25, "decision": "REJECT"}
    storage = Mock()
    storage.load.return_value = [existing_entry]
    history = HistoricalPerformance(storage)

    history.add(
        {"value": 70},
        0.5,
        "ACCEPT",
        [{"rule": "ValueRule", "score": 1.0}],
        source="restart",
    )

    assert history.history == [
        existing_entry,
        {
            "data": {"value": 70},
            "total_score": 0.5,
            "decision": "ACCEPT",
            "details": [{"rule": "ValueRule", "score": 1.0}],
            "source": "restart",
        },
    ]
    storage.save.assert_called_once_with(history.history)


def test_accepts_empty_history_from_storage():
    storage = Mock()
    storage.load.return_value = []

    history = HistoricalPerformance(storage)

    assert history.history == []
    storage.save.assert_not_called()


def test_rejects_malformed_history_from_storage():
    storage = Mock()
    storage.load.return_value = None

    with pytest.raises(TypeError, match=r"storage\.load\(\) must return a list"):
        HistoricalPerformance(storage)
