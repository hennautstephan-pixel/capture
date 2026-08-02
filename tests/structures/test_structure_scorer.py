from capture_recovery.models import (
    DataType,
    Detection,
)

from capture_recovery.structures import (
    Cluster,
    StructureCandidate,
    StructureScorer,
    ScoreBreakdown,
)


def detection(
    offset: int,
    length: int = 4,
    confidence: float = 1.0,
) -> Detection:

    return Detection(
        offset=offset,
        length=length,
        datatype=DataType.INT32,
        value=offset,
        confidence=confidence,
    )


def candidate(
    offset: int = 0,
    count: int = 4,
    spacing: int = 4,
    confidence: float = 1.0,
):

    detections = tuple(
        detection(
            offset + i * spacing,
            confidence=confidence,
        )
        for i in range(count)
    )

    return StructureCandidate(
        Cluster(detections)
    )


def test_create():

    scorer = StructureScorer()

    assert scorer is not None


def test_score_returns_float():

    scorer = StructureScorer()

    value = scorer.score(
        candidate()
    )

    assert isinstance(
        value,
        float,
    )


def test_score_range():

    scorer = StructureScorer()

    value = scorer.score(
        candidate()
    )

    assert 0.0 <= value <= 100.0


def test_evaluate():

    scorer = StructureScorer()

    result = scorer.evaluate(
        candidate()
    )

    assert isinstance(
        result,
        ScoreBreakdown,
    )


def test_candidate_updated():

    scorer = StructureScorer()

    c = candidate()

    value = scorer.score(c)

    assert c.score == value

    assert c.confidence == value


def test_alignment_score():

    scorer = StructureScorer()

    aligned = candidate(offset=16)

    unaligned = candidate(offset=3)

    assert (
        scorer._alignment_score(aligned)
        >
        scorer._alignment_score(
            unaligned,
        )
    )


def test_density_score():

    scorer = StructureScorer()

    c = candidate()

    assert (
        scorer._density_score(c)
        <= 1.0
    )


def test_field_score():

    scorer = StructureScorer()

    small = candidate(count=2)

    large = candidate(count=32)

    assert (
        scorer._field_score(large)
        >
        scorer._field_score(small)
    )


def test_callable():

    scorer = StructureScorer()

    c = candidate()

    assert scorer(c) == scorer.score(c)


def test_breakdown_total():

    scorer = StructureScorer()

    result = scorer.evaluate(
        candidate()
    )

    assert result.total >= 0.0


def test_breakdown_fields():

    scorer = StructureScorer()

    result = scorer.evaluate(
        candidate()
    )

    assert result.alignment >= 0

    assert result.density >= 0

    assert result.confidence >= 0

    assert result.field_count >= 0