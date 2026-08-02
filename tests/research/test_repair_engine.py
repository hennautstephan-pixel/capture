from capture_recovery.research import (
    RepairEngine,
    RepairEngineResult,
)


def test_engine_creation():

    engine = RepairEngine()

    assert isinstance(
        engine,
        RepairEngine,
    )


def test_result_properties():

    result = RepairEngineResult(
        integrity=None,
        rebuild=None,
        success=False,
    )

    assert result.success is False