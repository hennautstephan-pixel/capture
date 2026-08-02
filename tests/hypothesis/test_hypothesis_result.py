from capture_recovery.hypothesis import (
    Hypothesis,
    HypothesisResult,
)

from capture_recovery.models import (
    Detection,
    DataType,
)

from capture_recovery.structures import (
    Cluster,
    StructureCandidate,
)


def detection(offset):

    return Detection(
        offset=offset,
        length=4,
        datatype=DataType.INT32,
        value=offset,
    )


def candidate():

    return StructureCandidate(
        Cluster(
            (
                detection(0),
                detection(4),
            )
        )
    )


def hypothesis(confidence):

    return Hypothesis(
        object_type="Fixture",
        confidence=confidence,
        candidate=candidate(),
    )


def test_empty():

    result = HypothesisResult()

    assert result.empty

    assert result.best() is None


def test_add():

    result = HypothesisResult()

    result.add(
        hypothesis(80),
    )

    assert len(result) == 1


def test_best():

    result = HypothesisResult()

    result.add(
        hypothesis(80),
    )

    result.add(
        hypothesis(95),
    )

    assert result.best().confidence == 95


def test_confidence():

    result = HypothesisResult()

    result.add(
        hypothesis(87),
    )

    assert result.confidence == 87


def test_top():

    result = HypothesisResult()

    for value in (
        40,
        60,
        80,
        100,
    ):

        result.add(
            hypothesis(value),
        )

    assert len(
        result.top(2)
    ) == 2


def test_above():

    result = HypothesisResult()

    result.extend(
        [
            hypothesis(40),
            hypothesis(80),
            hypothesis(90),
        ]
    )

    assert len(
        result.above(70)
    ) == 2


def test_by_type():

    result = HypothesisResult()

    result.add(
        hypothesis(80),
    )

    assert len(
        result.by_type(
            "Fixture",
        )
    ) == 1


def test_clear():

    result = HypothesisResult()

    result.add(
        hypothesis(80),
    )

    result.clear()

    assert result.empty


def test_iter():

    result = HypothesisResult()

    result.add(
        hypothesis(80),
    )

    assert list(result)


def test_repr():

    result = HypothesisResult()

    assert "HypothesisResult" in repr(result)