from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterator

from capture_recovery.core.recovered_value import RecoveredValue
from capture_recovery.core.value_clusterer import ValueCluster, ValueClusterer


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def test_empty_input() -> None:
    clusterer = ValueClusterer()

    assert clusterer.cluster([]) == []


def test_single_value_creates_one_cluster() -> None:
    clusterer = ValueClusterer()
    value = RecoveredValue(type="string", value="demo", offset=10, size=4)

    clusters = clusterer.cluster([value])

    assert len(clusters) == 1
    assert clusters[0].values == (value,)


def test_multiple_values_are_grouped_when_close() -> None:
    clusterer = ValueClusterer(max_gap=64)
    values = [
        RecoveredValue(type="string", value="a", offset=10, size=4),
        RecoveredValue(type="uuid", value="uuid-1", offset=20, size=16),
        RecoveredValue(type="float", value=1.2, offset=30, size=8),
    ]

    clusters = clusterer.cluster(values)

    assert len(clusters) == 1
    assert clusters[0].size == 3
    assert clusters[0].values == tuple(values)


def test_values_inside_cluster_are_sorted() -> None:
    clusterer = ValueClusterer(max_gap=64)
    values = [
        RecoveredValue(type="float", value=1.2, offset=30, size=8),
        RecoveredValue(type="string", value="a", offset=10, size=4),
        RecoveredValue(type="uuid", value="uuid-1", offset=20, size=16),
    ]

    clusters = clusterer.cluster(values)

    assert len(clusters) == 1
    assert [value.offset for value in clusters[0].values] == [10, 20, 30]


def test_cluster_properties() -> None:
    value = RecoveredValue(type="string", value="demo", offset=10, size=4)
    cluster = ValueCluster(values=(value,))

    assert cluster.start_offset == 10
    assert cluster.end_offset == 14
    assert cluster.size == 1


def test_generator_input() -> None:
    clusterer = ValueClusterer()

    def generate_values() -> Iterator[RecoveredValue]:
        yield RecoveredValue(type="string", value="a", offset=10, size=4)
        yield RecoveredValue(type="uuid", value="uuid-1", offset=20, size=16)

    list_result = clusterer.cluster([
        RecoveredValue(type="string", value="a", offset=10, size=4),
        RecoveredValue(type="uuid", value="uuid-1", offset=20, size=16),
    ])
    generator_result = clusterer.cluster(generate_values())

    assert generator_result == list_result
