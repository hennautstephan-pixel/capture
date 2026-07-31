from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Mapping

from capture_recovery.core.recovered_value import RecoveredValue
from capture_recovery.core.value_clusterer import ValueCluster


@dataclass(frozen=True, slots=True)
class RecoveredValueStatistics:
    """Aggregate statistics about recovered values across a corpus."""

    total_values: int
    """The total number of recovered values seen."""

    by_type: Mapping[str, int]
    """A mapping of recovered value types to their occurrence count."""

    average_size: float
    """The average size of recovered values in bytes."""

    average_confidence: float
    """The average confidence score of recovered values."""


@dataclass(frozen=True, slots=True)
class ClusterPattern:
    """A recurring combination of recovered value types inside a cluster."""

    types: tuple[str, ...]
    """The sorted tuple of recovered value types present in the cluster."""

    count: int
    """The number of times this pattern was observed."""

    average_cluster_size: float
    """The average number of recovered values for clusters matching this pattern."""


@dataclass(frozen=True, slots=True)
class CorpusStatistics:
    """Summary statistics for a corpus of value clusters."""

    files_analyzed: int
    """The number of files or corpus entries analyzed."""

    total_recovered_values: int
    """The total number of recovered values seen across the corpus."""

    total_clusters: int
    """The total number of clusters seen across the corpus."""

    fixture_candidates: int
    """The number of clusters that contain both UUID and string values."""

    unknown_clusters: int
    """The number of clusters that are not fixture candidates."""

    value_statistics: RecoveredValueStatistics
    """Statistics aggregated over recovered values."""

    most_common_patterns: tuple[ClusterPattern, ...]
    """The most frequent cluster type patterns, sorted by frequency and name."""


class CaptureCorpusAnalyzer:
    """Analyze a corpus of value clusters without reconstructing fixtures."""

    def analyze(self, corpus: Iterable[Iterable[ValueCluster]]) -> CorpusStatistics:
        """Compute aggregate diagnostics for a corpus of cluster collections.

        The corpus is treated as an iterable of files, where each file is itself
        an iterable of value clusters. The method performs a single pass over the
        data to compute counts, averages, and the most frequent cluster patterns.
        """
        files: list[Iterable[ValueCluster]] = list(corpus)
        files_analyzed = len(files)

        total_recovered_values = 0
        total_clusters = 0
        fixture_candidates = 0
        total_value_size = 0
        total_value_confidence = 0.0
        type_counter: Counter[str] = Counter()
        pattern_counter: Counter[tuple[str, ...]] = Counter()
        cluster_size_total = 0

        for clusters in files:
            for cluster in clusters:
                total_clusters += 1
                cluster_size = len(cluster.values)
                cluster_size_total += cluster_size

                has_uuid = any(value.type == "uuid" for value in cluster.values)
                has_name = any(value.type == "string" for value in cluster.values)
                if has_uuid and has_name:
                    fixture_candidates += 1

                pattern_types = tuple(sorted({value.type for value in cluster.values}))
                pattern_counter[pattern_types] += 1

                for value in cluster.values:
                    total_recovered_values += 1
                    total_value_size += value.size
                    total_value_confidence += value.confidence
                    type_counter[value.type] += 1

        average_value_size = total_value_size / total_recovered_values if total_recovered_values else 0.0
        average_value_confidence = total_value_confidence / total_recovered_values if total_recovered_values else 0.0
        average_cluster_size = cluster_size_total / total_clusters if total_clusters else 0.0

        pattern_cluster_sizes: dict[tuple[str, ...], int] = {}
        for clusters in files:
            for cluster in clusters:
                pattern_types = tuple(sorted({value.type for value in cluster.values}))
                pattern_cluster_sizes[pattern_types] = pattern_cluster_sizes.get(pattern_types, 0) + len(cluster.values)

        patterns = [
            ClusterPattern(
                types=pattern,
                count=count,
                average_cluster_size=pattern_cluster_sizes[pattern] / count if count else 0.0,
            )
            for pattern, count in pattern_counter.items()
        ]
        patterns.sort(key=lambda item: (-item.count, item.types))

        return CorpusStatistics(
            files_analyzed=files_analyzed,
            total_recovered_values=total_recovered_values,
            total_clusters=total_clusters,
            fixture_candidates=fixture_candidates,
            unknown_clusters=total_clusters - fixture_candidates,
            value_statistics=RecoveredValueStatistics(
                total_values=total_recovered_values,
                by_type=dict(type_counter),
                average_size=average_value_size,
                average_confidence=average_value_confidence,
            ),
            most_common_patterns=tuple(patterns),
        )
