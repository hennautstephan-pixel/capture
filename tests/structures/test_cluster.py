from capture_recovery.models import (
    DataType,
    Detection,
)

from capture_recovery.structures.cluster import (
    Cluster,
)


def make_detection(
    offset: int,
    length: int = 4,
) -> Detection:

    return Detection(
        offset=offset,
        length=length,
        datatype=DataType.INT32,
        value=offset,
    )


def test_create_cluster():

    cluster = Cluster(
        (
            make_detection(0),
            make_detection(4),
            make_detection(8),
        )
    )

    assert cluster.start == 0
    assert cluster.end == 12
    assert cluster.span == 12
    assert cluster.size == 12
    assert cluster.detection_count == 3


def test_cluster_sorted():

    cluster = Cluster(
        (
            make_detection(8),
            make_detection(0),
            make_detection(4),
        )
    )

    assert cluster.first().offset == 0
    assert cluster.last().offset == 8


def test_contains():

    cluster = Cluster(
        (
            make_detection(0),
            make_detection(4),
        )
    )

    assert cluster.contains(2)
    assert cluster.contains(7)

    assert not cluster.contains(8)


def test_overlap():

    a = Cluster(
        (
            make_detection(0),
            make_detection(4),
        )
    )

    b = Cluster(
        (
            make_detection(6),
        )
    )

    assert a.overlaps(b)


def test_not_overlap():

    a = Cluster(
        (
            make_detection(0),
        )
    )

    b = Cluster(
        (
            make_detection(20),
        )
    )

    assert not a.overlaps(b)


def test_adjacent():

    a = Cluster(
        (
            make_detection(0),
        )
    )

    b = Cluster(
        (
            make_detection(4),
        )
    )

    assert a.adjacent(b)


def test_distance():

    a = Cluster(
        (
            make_detection(0),
        )
    )

    b = Cluster(
        (
            make_detection(20),
        )
    )

    assert a.distance_to(b) == 16


def test_merge():

    a = Cluster(
        (
            make_detection(0),
        )
    )

    b = Cluster(
        (
            make_detection(8),
        )
    )

    merged = a.merge(b)

    assert merged.detection_count == 2

    assert merged.start == 0

    assert merged.end == 12


def test_len():

    cluster = Cluster(
        (
            make_detection(0),
            make_detection(4),
            make_detection(8),
        )
    )

    assert len(cluster) == 3


def test_iter():

    cluster = Cluster(
        (
            make_detection(0),
            make_detection(4),
        )
    )

    offsets = [
        d.offset
        for d in cluster
    ]

    assert offsets == [0, 4]


def test_empty_cluster():

    import pytest

    with pytest.raises(
        ValueError,
    ):
        Cluster(())