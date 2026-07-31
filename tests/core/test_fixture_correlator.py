from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterator

from capture_recovery.core.fixture_correlator import FixtureCorrelator
from capture_recovery.core.recovered_value import RecoveredValue
from capture_recovery.core.semantic_correlator import SemanticCorrelator
from capture_recovery.core.value_clusterer import ValueCluster


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def test_fixture_correlator_inherits_semantic_correlator() -> None:
    correlator = FixtureCorrelator()

    assert isinstance(correlator, SemanticCorrelator)


def test_correlate_empty_list() -> None:
    correlator = FixtureCorrelator()

    assert correlator.correlate([]) == []


def test_correlate_single_cluster() -> None:
    correlator = FixtureCorrelator()
    rv1 = RecoveredValue(type="string", value="Robe", offset=10, size=4)
    rv2 = RecoveredValue(type="uuid", value="123e4567-e89b-12d3-a456-426614174000", offset=20, size=16)
    rv3 = RecoveredValue(type="float", value=1.5, offset=30, size=8)
    cluster = ValueCluster(values=(rv1, rv2, rv3))

    result = correlator.correlate([cluster])

    assert len(result) == 1
    assert result[0].object_type == "fixture"
    assert result[0].properties["uuid"] == rv2.value
    assert result[0].properties["name"] == "Robe"
    assert result[0].properties["values"] == (rv1, rv2, rv3)
    assert result[0].confidence == 0.75
    assert result[0].source_offsets == (10, 20, 30)


def test_correlate_generator() -> None:
    def generate_values() -> Iterator[ValueCluster]:
        yield ValueCluster(values=(RecoveredValue(type="string", value="Robe", offset=10, size=4),))
        yield ValueCluster(values=(RecoveredValue(type="uuid", value="123e4567-e89b-12d3-a456-426614174000", offset=20, size=16),))

    correlator = FixtureCorrelator()
    result = correlator.correlate(generate_values())

    assert len(result) == 2


def test_correlate_returns_new_list() -> None:
    correlator = FixtureCorrelator()

    first = correlator.correlate([])
    second = correlator.correlate([])

    assert first == []
    assert second == []
    assert first is not second


def test_correlate_never_modifies_input() -> None:
    correlator = FixtureCorrelator()
    clusters = [ValueCluster(values=(RecoveredValue(type="string", value="Robe", offset=10, size=4),))]
    original = clusters.copy()

    correlator.correlate(clusters)

    assert clusters == original
