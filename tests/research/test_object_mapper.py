from __future__ import annotations

from capture_recovery.research import (
    CandidateObject,
    CorrelationReport,
    FieldCorrelation,
    ObjectMap,
    ObjectMapper,
)


def create_field(
    offset: int,
    length: int,
    *,
    confidence: float = 1.0,
):

    return FieldCorrelation(
        offset=offset,
        length=length,
        confidence=confidence,
        type_candidates=("bytes",),
        evidence=("test",),
        occurrence_count=1,
    )


def test_empty():

    mapper = ObjectMapper()

    result = mapper.map(
        CorrelationReport([])
    )

    assert isinstance(
        result,
        ObjectMap,
    )

    assert result.object_count == 0


def test_single():

    mapper = ObjectMapper()

    result = mapper.map(
        CorrelationReport(
            [
                create_field(
                    100,
                    8,
                )
            ]
        )
    )

    assert result.object_count == 1

    assert isinstance(
        result.objects[0],
        CandidateObject,
    )


def test_overlap():

    mapper = ObjectMapper()

    result = mapper.map(
        CorrelationReport(
            [
                create_field(
                    100,
                    10,
                ),
                create_field(
                    105,
                    8,
                ),
            ]
        )
    )

    assert result.object_count == 1

    assert (
        result.objects[0].field_count
        == 2
    )


def test_gap():

    mapper = ObjectMapper()

    result = mapper.map(
        CorrelationReport(
            [
                create_field(
                    100,
                    10,
                ),
                create_field(
                    112,
                    5,
                ),
            ]
        ),
        max_gap=2,
    )

    assert result.object_count == 1


def test_no_gap():

    mapper = ObjectMapper()

    result = mapper.map(
        CorrelationReport(
            [
                create_field(
                    100,
                    10,
                ),
                create_field(
                    112,
                    5,
                ),
            ]
        )
    )

    assert result.object_count == 2


def test_by_offset():

    mapper = ObjectMapper()

    result = mapper.map(
        CorrelationReport(
            [
                create_field(
                    300,
                    5,
                ),
                create_field(
                    100,
                    5,
                ),
            ]
        )
    )

    ordered = result.by_offset()

    assert ordered[0].offset == 100

    assert ordered[1].offset == 300


def test_by_confidence():

    mapper = ObjectMapper()

    result = mapper.map(
        CorrelationReport(
            [
                create_field(
                    100,
                    5,
                    confidence=0.2,
                ),
                create_field(
                    300,
                    5,
                    confidence=0.9,
                ),
            ]
        )
    )

    ordered = result.by_confidence()

    assert (
        ordered[0].confidence
        >= ordered[1].confidence
    )


def test_end():

    mapper = ObjectMapper()

    result = mapper.map(
        CorrelationReport(
            [
                create_field(
                    100,
                    8,
                )
            ]
        )
    )

    obj = result.objects[0]

    assert obj.end == 108