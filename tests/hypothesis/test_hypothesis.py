from capture_recovery.hypothesis import Hypothesis

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


def candidate():

    return StructureCandidate(
        Cluster(
            (
                detection(0),
                detection(4),
                detection(8),
            )
        )
    )


def test_create():

    hypothesis = Hypothesis(
        object_type="Fixture",
        confidence=98.5,
        candidate=candidate(),
    )

    assert hypothesis.object_type == "Fixture"

    assert hypothesis.confidence == 98.5


def test_geometry():

    h = Hypothesis(
        object_type="Fixture",
        confidence=90,
        candidate=candidate(),
    )

    assert h.offset == 0

    assert h.length == 12

    assert h.end == 12


def test_field_count():

    h = Hypothesis(
        object_type="Fixture",
        confidence=90,
        candidate=candidate(),
    )

    assert h.field_count == 3


def test_score():

    c = candidate()

    c.score = 87.5

    h = Hypothesis(
        object_type="Fixture",
        confidence=90,
        candidate=c,
    )

    assert h.score == 87.5


def test_density():

    h = Hypothesis(
        object_type="Fixture",
        confidence=90,
        candidate=candidate(),
    )

    assert h.density > 0


def test_metadata():

    h = Hypothesis(
        object_type="Fixture",
        confidence=90,
        candidate=candidate(),
    )

    h.set(
        "version",
        "2024",
    )

    assert (
        h.get(
            "version",
        )
        == "2024"
    )


def test_metadata_default():

    h = Hypothesis(
        object_type="Fixture",
        confidence=90,
        candidate=candidate(),
    )

    assert (
        h.get(
            "unknown",
            123,
        )
        == 123
    )


def test_sort():

    a = Hypothesis(
        object_type="Fixture",
        confidence=80,
        candidate=candidate(),
    )

    b = Hypothesis(
        object_type="Layer",
        confidence=95,
        candidate=candidate(),
    )

    hypotheses = [
        a,
        b,
    ]

    hypotheses.sort()

    assert hypotheses[-1].confidence == 95


def test_repr():

    h = Hypothesis(
        object_type="Fixture",
        confidence=99,
        candidate=candidate(),
    )

    assert "Hypothesis" in repr(h)