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


def test_create_candidate():

    cluster = Cluster(
        (
            detection(0),
            detection(4),
            detection(8),
        )
    )

    candidate = StructureCandidate(cluster)

    assert candidate.offset == 0

    assert candidate.length == 12

    assert candidate.field_count == 3


def test_default_values():

    candidate = StructureCandidate(
        Cluster(
            (
                detection(0),
            )
        )
    )

    assert candidate.estimated_type == "Unknown"

    assert candidate.score == 0.0

    assert candidate.confidence == 0.0


def test_density():

    cluster = Cluster(
        (
            detection(0, 4),
            detection(8, 4),
        )
    )

    candidate = StructureCandidate(cluster)

    assert candidate.density == 8 / 12


def test_average_confidence():

    cluster = Cluster(
        (
            detection(0, confidence=0.5),
            detection(4, confidence=1.0),
        )
    )

    candidate = StructureCandidate(cluster)

    assert candidate.average_confidence == 0.75


def test_metadata():

    candidate = StructureCandidate(
        Cluster(
            (
                detection(0),
            )
        )
    )

    candidate.set(
        "version",
        "2024",
    )

    assert (
        candidate.get(
            "version",
        )
        == "2024"
    )


def test_metadata_default():

    candidate = StructureCandidate(
        Cluster(
            (
                detection(0),
            )
        )
    )

    assert (
        candidate.get(
            "unknown",
            123,
        )
        == 123
    )


def test_len():

    candidate = StructureCandidate(
        Cluster(
            (
                detection(0),
                detection(4),
                detection(8),
            )
        )
    )

    assert len(candidate) == 3


def test_iteration():

    candidate = StructureCandidate(
        Cluster(
            (
                detection(0),
                detection(4),
            )
        )
    )

    offsets = [
        d.offset
        for d in candidate
    ]

    assert offsets == [0, 4]


def test_repr():

    candidate = StructureCandidate(
        Cluster(
            (
                detection(0),
            )
        )
    )

    assert "StructureCandidate" in repr(candidate)


def test_end():

    candidate = StructureCandidate(
        Cluster(
            (
                detection(10),
                detection(20),
            )
        )
    )

    assert candidate.end == 24