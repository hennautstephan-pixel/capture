from __future__ import annotations

import sys
from pathlib import Path

from capture_recovery.analysis.corpus_analyzer import (
    CaptureCorpusAnalyzer,
    ClusterPattern,
    CorpusStatistics,
    RecoveredValueStatistics,
)
from capture_recovery.core.recovered_value import RecoveredValue
from capture_recovery.core.value_clusterer import ValueCluster


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def test_corpus_analyzer_statistics() -> None:
    analyzer = CaptureCorpusAnalyzer()
    corpus = [
        [
            ValueCluster(values=(
                RecoveredValue(type="uuid", value="abc", offset=10, size=16, confidence=0.9),
                RecoveredValue(type="string", value="Robe", offset=20, size=4, confidence=0.8),
            )),
            ValueCluster(values=(
                RecoveredValue(type="int", value=1, offset=30, size=4, confidence=0.7),
                RecoveredValue(type="int", value=2, offset=34, size=4, confidence=0.6),
            )),
        ],
        [
            ValueCluster(values=(
                RecoveredValue(type="float", value=1.5, offset=40, size=8, confidence=0.5),
                RecoveredValue(type="string", value="Test", offset=48, size=4, confidence=0.4),
            )),
        ],
    ]

    statistics = analyzer.analyze(corpus)

    assert statistics.files_analyzed == 2
    assert statistics.total_recovered_values == 6
    assert statistics.total_clusters == 3
    assert statistics.fixture_candidates == 1
    assert statistics.unknown_clusters == 2
    assert statistics.value_statistics == RecoveredValueStatistics(
        total_values=6,
        by_type={"uuid": 1, "string": 2, "int": 2, "float": 1},
        average_size=(16 + 4 + 4 + 4 + 8 + 4) / 6,
        average_confidence=(0.9 + 0.8 + 0.7 + 0.6 + 0.5 + 0.4) / 6,
    )
    assert statistics.most_common_patterns == (
        ClusterPattern(types=("float", "string"), count=1, average_cluster_size=2.0),
        ClusterPattern(types=("int",), count=1, average_cluster_size=2.0),
        ClusterPattern(types=("string", "uuid"), count=1, average_cluster_size=2.0),
    )


def test_corpus_analyzer_empty_corpus() -> None:
    analyzer = CaptureCorpusAnalyzer()

    statistics = analyzer.analyze([])

    assert statistics == CorpusStatistics(
        files_analyzed=0,
        total_recovered_values=0,
        total_clusters=0,
        fixture_candidates=0,
        unknown_clusters=0,
        value_statistics=RecoveredValueStatistics(
            total_values=0,
            by_type={},
            average_size=0.0,
            average_confidence=0.0,
        ),
        most_common_patterns=(),
    )
