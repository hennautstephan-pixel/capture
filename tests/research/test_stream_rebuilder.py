from __future__ import annotations

from capture_recovery.research import (
    CandidateObject,
    ExecutionPlan,
    RepairAction,
    RepairOperation,
    RepairPlan,
    RepairPlanner,
    RepairPriority,
    RepairStep,
    StreamRebuilder,
    StreamRebuildResult,
)


def create_plan():

    planner = RepairPlanner()

    return planner.build(
        RepairPlan(
            [
                RepairStep(
                    RepairAction.REPAIR_STREAM,
                    "",
                    RepairPriority.STREAM,
                )
            ],
            1.0,
        )
    )


def create_object(
    data: bytes = b"",
):

    return CandidateObject(
        offset=0,
        length=len(data),
        confidence=1.0,
        fields=(),
        data=data,
    )


def test_empty():

    rebuilder = StreamRebuilder()

    result = rebuilder.rebuild(
        ExecutionPlan([]),
        [],
    )

    assert isinstance(
        result,
        StreamRebuildResult,
    )

    assert result.size == 0

    assert result.repaired_objects == 0


def test_rebuild():

    rebuilder = StreamRebuilder()

    obj = create_object(b"abcd")

    result = rebuilder.rebuild(
        create_plan(),
        [obj],
    )

    assert result.size == 4

    assert result.repaired_objects == 1

    assert result.stream == b"abcd"


def test_chunks():

    rebuilder = StreamRebuilder()

    obj = create_object(b"abcd")

    result = rebuilder.rebuild(
        create_plan(),
        [obj],
    )

    assert len(result.chunks) == 1

    assert result.chunks[0].offset == 0

    assert result.chunks[0].length == 4


def test_no_rebuild():

    planner = RepairPlanner()

    plan = planner.build(
        RepairPlan([], 1.0)
    )

    rebuilder = StreamRebuilder()

    result = rebuilder.rebuild(
        plan,
        [],
    )

    assert result.size == 0

    assert result.repaired_objects == 0


def test_stream_content():

    rebuilder = StreamRebuilder()

    obj = create_object(b"1234")

    result = rebuilder.rebuild(
        create_plan(),
        [obj],
    )

    assert result.stream == b"1234"

    assert result.chunks[0].data == b"1234"