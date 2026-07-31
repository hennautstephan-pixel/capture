from __future__ import annotations

import sys
from pathlib import Path

from capture_recovery.core.cluster_analyzer import ClusterAnalyzer, ClusterStatistics
from capture_recovery.core.recovered_value import RecoveredValue
from capture_recovery.core.value_clusterer import ValueCluster


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def test_cluster_analyzer_statistics() -> None:
    analyzer = ClusterAnalyzer()
    clusters = [
        ValueCluster(values=(
            RecoveredValue(type="uuid", value="abc", offset=10, size=16),
            RecoveredValue(type="string", value="Robe", offset=20, size=4),
            RecoveredValue(type="int", value=1, offset=30, size=4),
        )),
        ValueCluster(values=(
            RecoveredValue(type="string", value="Test", offset=40, size=4),
            RecoveredValue(type="int", value=200, offset=50, size=4),
        )),
        ValueCluster(values=(
            RecoveredValue(type="float", value=1.5, offset=60, size=8),
        )),
    ]

    statistics = analyzer.analyze(clusters)

    assert statistics == ClusterStatistics(
        total_clusters=3,
        fixture_candidates=1,
        unknown_clusters=2,
        clusters_with_uuid=1,
        clusters_with_name=2,
        clusters_with_dmx=2,
        average_cluster_size=2.0,
    )


def test_cluster_analyzer_empty_input() -> None:
    analyzer = ClusterAnalyzer()

    statistics = analyzer.analyze([])

    assert statistics == ClusterStatistics(
        total_clusters=0,
        fixture_candidates=0,
        unknown_clusters=0,
        clusters_with_uuid=0,
        clusters_with_name=0,
        clusters_with_dmx=0,
        average_cluster_size=0.0,
    )
