from capture_recovery.hypothesis import (
    Hypothesis,
    HypothesisEngine,
    HypothesisResult,
)

from capture_recovery.models import (
    DataType,
    Detection,
)

from capture_recovery.structures import (
    Cluster,
    StructureCandidate,
)


def detection(
    offset: int,
    confidence: float = 1.0,
) -> Detection:

    return Detection(
        offset=offset,
        length=4,
        datatype=DataType.INT32,
        value=offset,
        confidence=confidence,
    )


def candidate(
    score: float,
):

    cluster = Cluster(
        (
            detection(0),
            detection(4),
            detection(8),
        )
    )

    c = StructureCandidate(
        cluster,
    )

    c.score = score
    c.confidence = score

    return c


def test_create():

    engine = HypothesisEngine()

    assert engine is not None


def test_infer_returns_result():

    engine = HypothesisEngine()

    result = engine.infer(
        candidate(95),
    )

    assert isinstance(
        result,
        HypothesisResult,
    )


def test_callable():

    engine = HypothesisEngine()

    result = engine(
        candidate(95),
    )

    assert isinstance(
        result,
        HypothesisResult,
    )


def test_result_not_empty():

    engine = HypothesisEngine()

    result = engine.infer(
        candidate(95),
    )

    assert len(result) > 0


def test_best():

    engine = HypothesisEngine()

    result = engine.infer(
        candidate(95),
    )

    assert isinstance(
        result.best(),
        Hypothesis,
    )


def test_structure_candidate():

    engine = HypothesisEngine()

    result = engine.infer(
        candidate(95),
    )

    assert (
        result.best().object_type
        == "Structure"
    )


def test_possible_structure():

    engine = HypothesisEngine()

    result = engine.infer(
        candidate(80),
    )

    assert (
        result.best().object_type
        == "PossibleStructure"
    )


def test_unknown():

    engine = HypothesisEngine()

    result = engine.infer(
        candidate(20),
    )

    assert (
        result.best().object_type
        == "Unknown"
    )


def test_sorted():

    engine = HypothesisEngine()

    result = engine.infer(
        candidate(95),
    )

    confidences = [
        h.confidence
        for h in result
    ]

    assert confidences == sorted(
        confidences,
        reverse=True,
    )


def test_best_confidence():

    engine = HypothesisEngine()

    result = engine.infer(
        candidate(95),
    )

    assert (
        result.best().confidence
        >=
        result[-1].confidence
    )