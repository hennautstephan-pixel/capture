from capture_recovery.indexes import DetectionIndex
from capture_recovery.models import (
    DataType,
    Detection,
)
from capture_recovery.structures import (
    Cluster,
    ClusterBuilder,
)


def detection(offset: int, length: int = 4) -> Detection:
    return Detection(
        offset=offset,
        length=length,
        datatype=DataType.INT32,
        value=offset,
    )


def test_empty_index():

    builder = ClusterBuilder()

    clusters = builder.build(
        DetectionIndex([])
    )

    assert clusters == []


def test_single_cluster():

    index = DetectionIndex(
        [
            detection(0),
            detection(4),
            detection(8),
        ]
    )

    builder = ClusterBuilder()

    clusters = builder.build(index)

    assert len(clusters) == 1

    cluster = clusters[0]

    assert isinstance(cluster, Cluster)

    assert cluster.start == 0

    assert cluster.end == 12

    assert cluster.detection_count == 3


def test_two_clusters():

    index = DetectionIndex(
        [
            detection(0),
            detection(4),
            detection(100),
            detection(104),
        ]
    )

    builder = ClusterBuilder()

    clusters = builder.build(index)

    assert len(clusters) == 2

    assert clusters[0].start == 0

    assert clusters[1].start == 100


def test_gap_parameter():

    index = DetectionIndex(
        [
            detection(0),
            detection(20),
        ]
    )

    builder = ClusterBuilder(
        max_gap=32,
    )

    clusters = builder.build(index)

    assert len(clusters) == 1


def test_gap_separation():

    index = DetectionIndex(
        [
            detection(0),
            detection(20),
        ]
    )

    builder = ClusterBuilder(
        max_gap=8,
    )

    clusters = builder.build(index)

    assert len(clusters) == 2


def test_call_operator():

    index = DetectionIndex(
        [
            detection(0),
        ]
    )

    builder = ClusterBuilder()

    clusters = builder(index)

    assert len(clusters) == 1


def test_cluster_order():

    index = DetectionIndex(
        [
            detection(100),
            detection(0),
            detection(4),
            detection(200),
        ]
    )

    builder = ClusterBuilder()

    clusters = builder.build(index)

    assert clusters[0].start == 0

    assert clusters[1].start == 100

    assert clusters[2].start == 200


def test_cluster_type():

    index = DetectionIndex(
        [
            detection(0),
        ]
    )

    builder = ClusterBuilder()

    clusters = builder.build(index)

    assert all(
        isinstance(c, Cluster)
        for c in clusters
    )