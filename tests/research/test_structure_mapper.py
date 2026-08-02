from __future__ import annotations

from capture_recovery.research import (
    CandidateStructure,
    MergedPatternRegion,
    MergedPatterns,
    PatternMerger,
    PatternRegion,
    StructureMap,
    StructureMapper,
)


def create_region(
    offset: int,
    length: int,
    occurrences: int,
) -> PatternRegion:

    return PatternRegion(
        offset=offset,
        length=length,
        occurrence_count=occurrences,
    )


def create_merged():

    merger = PatternMerger()

    patterns = MergedPatterns(
        regions=[
            merger._build_region(
                [
                    create_region(
                        100,
                        10,
                        5,
                    )
                ],
                100,
                110,
            ),
            merger._build_region(
                [
                    create_region(
                        300,
                        20,
                        3,
                    )
                ],
                300,
                320,
            ),
        ]
    )

    return patterns


def test_empty():

    mapper = StructureMapper()

    result = mapper.map(
        MergedPatterns([])
    )

    assert isinstance(
        result,
        StructureMap,
    )

    assert result.structure_count == 0


def test_map():

    mapper = StructureMapper()

    result = mapper.map(
        create_merged()
    )

    assert result.structure_count == 2

    assert isinstance(
        result.structures[0],
        CandidateStructure,
    )


def test_confidence():

    mapper = StructureMapper()

    result = mapper.map(
        create_merged()
    )

    confidence = (
        result.structures[0].confidence
    )

    assert 0.0 <= confidence <= 1.0


def test_evidence():

    mapper = StructureMapper()

    result = mapper.map(
        create_merged()
    )

    evidence = (
        result.structures[0].evidence
    )

    assert len(evidence) > 0


def test_end():

    mapper = StructureMapper()

    result = mapper.map(
        create_merged()
    )

    structure = result.structures[0]

    assert (
        structure.end
        == structure.offset
        + structure.length
    )


def test_by_offset():

    mapper = StructureMapper()

    result = mapper.map(
        create_merged()
    )

    ordered = result.by_offset()

    assert ordered[0].offset == 100

    assert ordered[1].offset == 300