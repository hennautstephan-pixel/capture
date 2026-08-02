from capture_recovery.recovery import (
    IntegrityReport,
    ProjectRepairEngine,
)


def test_returns_copy():

    engine = ProjectRepairEngine()

    project = {
        "scene": {
            "fixtures": [],
        },
    }

    repaired = engine.repair(
        project,
        IntegrityReport(),
    )

    assert repaired == project
    assert repaired is not project


def test_original_not_modified():

    engine = ProjectRepairEngine()

    project = {
        "value": 1,
    }

    repaired = engine.repair(
        project,
        IntegrityReport(),
    )

    repaired["value"] = 2

    assert project["value"] == 1


def test_repairs_initially_empty():

    engine = ProjectRepairEngine()

    engine.repair(
        {},
        IntegrityReport(),
    )

    assert engine.repairs == ()