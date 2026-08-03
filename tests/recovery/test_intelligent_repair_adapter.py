from capture_recovery.recovery import (
    AdaptedRepairPlan,
    IntelligentRepairAdapter,
    IntelligentRepairCandidate,
    IntelligentRepairResult,
)


def test_adapter_converts_candidate():

    candidate = IntelligentRepairCandidate(
        object_type="fixture",
        offset=100,
        size=500,
        confidence=0.9,
        evidence=(
            "matched corpus pattern",
        ),
    )

    result = IntelligentRepairResult(
        candidates=(
            candidate,
        ),
        repair_plan=None,
    )

    adapter = IntelligentRepairAdapter()

    adapted = adapter.adapt(
        result,
    )

    assert isinstance(
        adapted,
        AdaptedRepairPlan,
    )

    assert len(
        adapted.actions,
    ) == 1

    assert (
        adapted.actions[0].action_type
        == "restore_object"
    )