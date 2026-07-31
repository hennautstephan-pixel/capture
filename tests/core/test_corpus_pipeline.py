from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from capture_recovery.analysis.corpus_analyzer import (
    CaptureCorpusAnalyzer,
    CorpusStatistics,
    RecoveredValueStatistics,
)
from capture_recovery.analysis.corpus_pipeline import CaptureCorpusPipeline
from capture_recovery.core.recovered_value import RecoveredValue
from capture_recovery.core.value_clusterer import ValueCluster, ValueClusterer

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class StubInspector:
    def __init__(self, results: dict[bytes, list[RecoveredValue]] | None = None) -> None:
        self._results = results or {}
        self.calls: list[bytes] = []

    def inspect(self, data: bytes) -> list[RecoveredValue]:
        self.calls.append(data)
        return list(self._results.get(data, []))


class StubClusterer:
    def __init__(self) -> None:
        self.calls: list[tuple[RecoveredValue, ...]] = []

    def cluster(self, values: Any) -> list[ValueCluster]:
        ordered_values = tuple(values)
        self.calls.append(ordered_values)
        if not ordered_values:
            return []
        return [ValueCluster(values=ordered_values)]


class StubAnalyzer:
    def __init__(self, statistics: CorpusStatistics) -> None:
        self._statistics = statistics
        self.calls: list[list[list[ValueCluster]]] = []

    def analyze(self, corpus: list[list[ValueCluster]]) -> CorpusStatistics:
        self.calls.append(corpus)
        return self._statistics


def test_pipeline_accepts_empty_file() -> None:
    inspector = StubInspector()
    clusterer = StubClusterer()
    statistics = CorpusStatistics(
        files_analyzed=1,
        total_recovered_values=0,
        total_clusters=0,
        fixture_candidates=0,
        unknown_clusters=0,
        value_statistics=RecoveredValueStatistics(total_values=0, by_type={}, average_size=0.0, average_confidence=0.0),
        most_common_patterns=(),
    )
    analyzer = StubAnalyzer(statistics)
    pipeline = CaptureCorpusPipeline(inspector=inspector, clusterer=clusterer, analyzer=analyzer)

    result = pipeline.analyze_files([b""])

    assert result is statistics
    assert inspector.calls == [b""]
    assert clusterer.calls == [()]
    assert analyzer.calls == [[[]]]


def test_pipeline_invokes_each_dependency_once_per_file() -> None:
    first_value = RecoveredValue(type="uuid", value="abc", offset=0, size=16, confidence=1.0)
    second_value = RecoveredValue(type="string", value="name", offset=16, size=8, confidence=0.9)
    inspector = StubInspector({b"a": [first_value], b"b": [second_value]})
    clusterer = StubClusterer()
    statistics = CorpusStatistics(
        files_analyzed=2,
        total_recovered_values=2,
        total_clusters=2,
        fixture_candidates=0,
        unknown_clusters=2,
        value_statistics=RecoveredValueStatistics(total_values=2, by_type={"uuid": 1, "string": 1}, average_size=12.0, average_confidence=0.95),
        most_common_patterns=(),
    )
    analyzer = StubAnalyzer(statistics)
    pipeline = CaptureCorpusPipeline(inspector=inspector, clusterer=clusterer, analyzer=analyzer)

    pipeline.analyze_files([b"a", b"b"])

    assert inspector.calls == [b"a", b"b"]
    assert clusterer.calls == [(first_value,), (second_value,)]
    assert analyzer.calls == [[[ValueCluster(values=(first_value,))], [ValueCluster(values=(second_value,))]]]


def test_pipeline_returns_statistics_from_analyzer() -> None:
    inspector = StubInspector()
    clusterer = StubClusterer()
    expected = CorpusStatistics(
        files_analyzed=1,
        total_recovered_values=0,
        total_clusters=0,
        fixture_candidates=0,
        unknown_clusters=0,
        value_statistics=RecoveredValueStatistics(total_values=0, by_type={}, average_size=0.0, average_confidence=0.0),
        most_common_patterns=(),
    )
    analyzer = StubAnalyzer(expected)
    pipeline = CaptureCorpusPipeline(inspector=inspector, clusterer=clusterer, analyzer=analyzer)

    assert pipeline.analyze_files([b"data"]) is expected


def test_pipeline_does_not_transform_cluster_data() -> None:
    recovered_value = RecoveredValue(type="uuid", value="abc", offset=0, size=16, confidence=1.0)
    inspector = StubInspector({b"data": [recovered_value]})
    clusterer = StubClusterer()
    analyzer = StubAnalyzer(
        CorpusStatistics(
            files_analyzed=1,
            total_recovered_values=1,
            total_clusters=1,
            fixture_candidates=0,
            unknown_clusters=1,
            value_statistics=RecoveredValueStatistics(total_values=1, by_type={"uuid": 1}, average_size=16.0, average_confidence=1.0),
            most_common_patterns=(),
        )
    )
    pipeline = CaptureCorpusPipeline(inspector=inspector, clusterer=clusterer, analyzer=analyzer)

    pipeline.analyze_files([b"data"])

    assert analyzer.calls[0][0][0].values == (recovered_value,)
    assert analyzer.calls[0][0][0].values[0] is recovered_value
    assert clusterer.calls[0] == (recovered_value,)
