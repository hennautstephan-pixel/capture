from capture_recovery.tools import (
    DiffAnalysis,
    DiffRegion,
    ObjectIdentifier,
)


def test_large_region_is_object_candidate():

    analysis = DiffAnalysis(
        regions=(
            DiffRegion(
                start_offset=100,
                end_offset=700,
                differences=(),
            ),
        ),
    )

    identifier = ObjectIdentifier()

    result = identifier.identify(
        analysis,
    )

    assert result.candidate_count == 1

    candidate = result.candidates[0]

    assert candidate.object_type == "object"
    assert candidate.offset == 100
    assert candidate.size == 601
    assert candidate.confidence == 0.75