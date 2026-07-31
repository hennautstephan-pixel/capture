from __future__ import annotations

from typing import Iterable

from capture_recovery.analysis.corpus_analyzer import CaptureCorpusAnalyzer, CorpusStatistics
from capture_recovery.core.recovered_value import RecoveredValue
from capture_recovery.core.value_clusterer import ValueCluster, ValueClusterer
from capture_recovery.parser.binary_inspector import BinaryInspector


class CaptureCorpusPipeline:
    """Orchestrate inspection, clustering, and corpus analysis for a set of files."""

    def __init__(
        self,
        inspector: BinaryInspector,
        clusterer: ValueClusterer,
        analyzer: CaptureCorpusAnalyzer,
    ) -> None:
        """Store the injected dependencies used by the pipeline.

        Args:
            inspector: Component that inspects a binary payload and returns recovered values.
            clusterer: Component that groups recovered values into clusters.
            analyzer: Component that computes corpus-level statistics from the clusters.
        """
        self._inspector = inspector
        self._clusterer = clusterer
        self._analyzer = analyzer

    def analyze_files(self, files: Iterable[bytes]) -> CorpusStatistics:
        """Analyze each file through the existing inspection and clustering pipeline.

        The method does not add heuristics or transform the values produced by the
        injected components. It simply forwards each file through the configured
        dependency chain and returns the statistics emitted by the analyzer.
        """
        clustered_files: list[list[ValueCluster]] = []

        for file_bytes in files:
            recovered_values: Iterable[RecoveredValue] = self._inspector.inspect(file_bytes)
            clusters = self._clusterer.cluster(recovered_values)
            clustered_files.append(clusters)

        return self._analyzer.analyze(clustered_files)
