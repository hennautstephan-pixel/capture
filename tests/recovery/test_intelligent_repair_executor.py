from capture_recovery.recovery import (
    IntelligentRepairExecutor,
    IntelligentRestoreAction,
    AdaptedRepairPlan,
)


def test_executor_runs_high_confidence_action():

    action = IntelligentRestoreAction(
        offset=100,
        size=500,
        object_type="fixture",
        confidence=0.95,
    )

    plan = AdaptedRepairPlan(
        actions=(
            action,
        )
    )

    executor = IntelligentRepairExecutor()

    result = executor.execute(
        plan,
        project=None,
        report=None,
    )

    assert len(result.executed) == 1

    assert len(result.skipped) == 0



def test_executor_skips_low_confidence_action():

    action = IntelligentRestoreAction(
        offset=100,
        size=500,
        object_type="fixture",
        confidence=0.20,
    )

    plan = AdaptedRepairPlan(
        actions=(
            action,
        )
    )

    executor = IntelligentRepairExecutor()

    result = executor.execute(
        plan,
        project=None,
        report=None,
    )

    assert len(result.executed) == 0

    assert len(result.skipped) == 1