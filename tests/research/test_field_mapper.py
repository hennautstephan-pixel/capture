from __future__ import annotations

from capture_recovery.research import (
    CandidateStructure,
    FieldCandidate,
    FieldMap,
    FieldMapper,
    StructureMap,
)


def create_structure(
    offset: int,
    length: int,
    confidence: float = 1.0,
):

    return CandidateStructure(
        offset=offset,
        length=length,
        confidence=confidence,
        evidence=("test",),
    )


def test_empty():

    mapper = FieldMapper()

    result = mapper.map(
        StructureMap([])
    )

    assert isinstance(
        result,
        FieldMap,
    )

    assert result.field_count == 0


def test_single():

    mapper = FieldMapper()

    result = mapper.map(
        StructureMap(
            [
                create_structure(
                    100,
                    4,
                )
            ]
        )
    )

    assert result.field_count == 1

    assert isinstance(
        result.fields[0],
        FieldCandidate,
    )


def test_offset():

    mapper = FieldMapper()

    result = mapper.map(
        StructureMap(
            [
                create_structure(
                    123,
                    4,
                )
            ]
        )
    )

    assert (
        result.fields[0].offset
        == 123
    )


def test_end():

    mapper = FieldMapper()

    result = mapper.map(
        StructureMap(
            [
                create_structure(
                    100,
                    16,
                )
            ]
        )
    )

    field = result.fields[0]

    assert (
        field.end
        == 116
    )


def test_by_offset():

    mapper = FieldMapper()

    result = mapper.map(
        StructureMap(
            [
                create_structure(
                    300,
                    4,
                ),
                create_structure(
                    100,
                    4,
                ),
            ]
        )
    )

    ordered = result.by_offset()

    assert ordered[0].offset == 100

    assert ordered[1].offset == 300


def test_candidate_types():

    mapper = FieldMapper()

    result = mapper.map(
        StructureMap(
            [
                create_structure(
                    100,
                    4,
                )
            ]
        )
    )

    assert (
        "uint32"
        in result.fields[0].type_candidates
    )


def test_confidence():

    mapper = FieldMapper()

    result = mapper.map(
        StructureMap(
            [
                create_structure(
                    100,
                    8,
                    confidence=0.75,
                )
            ]
        )
    )

    assert (
        result.fields[0].confidence
        == 0.75
    )