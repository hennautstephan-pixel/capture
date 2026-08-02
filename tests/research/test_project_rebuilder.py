from __future__ import annotations

from capture_recovery.research import (
    ExecutionPlan,
    ProjectImage,
    ProjectRebuilder,
    ProjectRebuildResult,
    RebuiltChunk,
    StreamRebuildResult,
)


def create_stream():

    return StreamRebuildResult(
        chunks=[
            RebuiltChunk(
                offset=0,
                data=b"abcd",
            )
        ],
        stream=b"abcd",
        repaired_objects=1,
        warnings=(),
    )


def test_image():

    image = ProjectImage(
        header=b"H",
        stream=b"S",
        footer=b"F",
    )

    assert image.data == b"HSF"

    assert image.size == 3

    assert not image.is_empty


def test_empty():

    image = ProjectImage(
        header=b"",
        stream=b"",
        footer=b"",
    )

    assert image.is_empty


def test_rebuild():

    result = ProjectRebuilder().rebuild(
        ExecutionPlan([]),
        b"H",
        create_stream(),
        b"F",
    )

    assert result.repaired

    assert result.image.data == b"HabcdF"

    assert result.is_valid


def test_size():

    result = ProjectRebuilder().rebuild(
        ExecutionPlan([]),
        b"H",
        create_stream(),
        b"F",
    )

    assert result.image.size == 6


def test_warnings():

    stream = StreamRebuildResult(
        chunks=[],
        stream=b"",
        repaired_objects=0,
        warnings=("warning",),
    )

    result = ProjectRebuilder().rebuild(
        ExecutionPlan([]),
        b"",
        stream,
        b"",
    )

    assert len(result.warnings) >= 3

    assert not result.is_valid


def test_result_type():

    result = ProjectRebuilder().rebuild(
        ExecutionPlan([]),
        b"H",
        create_stream(),
        b"F",
    )

    assert isinstance(
        result,
        ProjectRebuildResult,
    )