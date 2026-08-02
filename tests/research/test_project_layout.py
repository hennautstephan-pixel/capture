from __future__ import annotations

from capture_recovery.research import (
    CandidateObject,
    FieldCorrelation,
    LayoutRegion,
    ObjectMap,
    ProjectLayout,
    ProjectLayoutBuilder,
)


def create_object(
    offset: int,
    length: int,
):

    field = FieldCorrelation(
        offset=offset,
        length=length,
        confidence=1.0,
        type_candidates=("bytes",),
        evidence=("test",),
        occurrence_count=1,
    )

    return CandidateObject(
        offset=offset,
        length=length,
        confidence=1.0,
        fields=(field,),
    )


def test_empty():

    builder = ProjectLayoutBuilder()

    layout = builder.build(
        file_size=100,
        header_size=10,
        stream_offset=10,
        stream_length=80,
        footer_size=10,
        objects=ObjectMap([]),
    )

    assert isinstance(
        layout,
        ProjectLayout,
    )

    assert layout.object_count == 0

    assert layout.gap_count == 1


def test_regions():

    builder = ProjectLayoutBuilder()

    layout = builder.build(
        file_size=200,
        header_size=20,
        stream_offset=20,
        stream_length=160,
        footer_size=20,
        objects=ObjectMap([]),
    )

    assert isinstance(
        layout.header,
        LayoutRegion,
    )

    assert layout.header.length == 20

    assert layout.stream.length == 160

    assert layout.footer.length == 20


def test_object_count():

    builder = ProjectLayoutBuilder()

    layout = builder.build(
        file_size=200,
        header_size=20,
        stream_offset=20,
        stream_length=160,
        footer_size=20,
        objects=ObjectMap(
            [
                create_object(
                    40,
                    20,
                )
            ]
        ),
    )

    assert layout.object_count == 1


def test_gap_detection():

    builder = ProjectLayoutBuilder()

    layout = builder.build(
        file_size=200,
        header_size=20,
        stream_offset=20,
        stream_length=160,
        footer_size=20,
        objects=ObjectMap(
            [
                create_object(
                    40,
                    20,
                ),
                create_object(
                    100,
                    20,
                ),
            ]
        ),
    )

    assert layout.gap_count == 3


def test_region_end():

    builder = ProjectLayoutBuilder()

    layout = builder.build(
        file_size=100,
        header_size=10,
        stream_offset=10,
        stream_length=80,
        footer_size=10,
        objects=ObjectMap([]),
    )

    assert layout.header.end == 10

    assert layout.stream.end == 90

    assert layout.footer.end == 100