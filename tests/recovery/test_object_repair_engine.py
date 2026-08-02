from capture_recovery.recovery import (
    IntegrityReport,
    ObjectRepairEngine,
)


def test_returns_copy():

    engine = ObjectRepairEngine()

    obj = {
        "name": "Fixture",
    }

    repaired = engine.repair(
        obj,
    )

    assert repaired == obj
    assert repaired is not obj


def test_original_not_modified():

    engine = ObjectRepairEngine()

    obj = {
        "value": 10,
    }

    repaired = engine.repair(
        obj,
    )

    repaired["value"] = 42

    assert obj["value"] == 10


def test_repairs_initially_empty():

    engine = ObjectRepairEngine()

    engine.repair(
        {},
        report=IntegrityReport(),
    )

    assert engine.repairs == ()