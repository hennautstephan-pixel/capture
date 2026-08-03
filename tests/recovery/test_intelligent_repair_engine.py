from capture_recovery.recovery import (
    IntelligentRepairEngine,
)


def test_engine_can_be_created():

    engine = IntelligentRepairEngine()

    assert engine is not None