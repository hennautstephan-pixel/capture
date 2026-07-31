from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from capture_recovery.core.value_clusterer import ValueCluster


@dataclass(frozen=True, slots=True)
class ClusterStatistics:
    """Statistical summary of a collection of value clusters."""

    total_clusters: int
    """The total number of clusters analyzed."""

    fixture_candidates: int
    """The number of clusters that look like fixture candidates."""

    unknown_clusters: int
    """The number of clusters that are not fixture candidates."""

    clusters_with_uuid: int
    """The number of clusters that contain at least one UUID."""

    clusters_with_name: int
    """The number of clusters that contain at least one string."""

    clusters_with_dmx: int
    """The number of clusters that contain DMX-related values."""

    average_cluster_size: float
    """The average number of recovered values per cluster."""


class ClusterAnalyzer:
    """Analyze value clusters for diagnostics without reconstruction."""

    def analyze(self, clusters: Iterable[ValueCluster]) -> ClusterStatistics:
        """Compute purely statistical metrics for the provided clusters."""
        cluster_list = list(clusters)
        total_clusters = len(cluster_list)

        fixture_candidates = 0
        clusters_with_uuid = 0
        clusters_with_name = 0
        clusters_with_dmx = 0

        total_size = 0
        for cluster in cluster_list:
            has_uuid = any(value.type == "uuid" for value in cluster.values)
            has_name = any(value.type == "string" for value in cluster.values)
            has_dmx = any(
                value.type == "int"
                and isinstance(value.value, int)
                and 1 <= value.value <= 512
                for value in cluster.values
            )

            if has_uuid and has_name:
                fixture_candidates += 1
            if has_uuid:
                clusters_with_uuid += 1
            if has_name:
                clusters_with_name += 1
            if has_dmx:
                clusters_with_dmx += 1

            total_size += len(cluster.values)

        average_cluster_size = total_size / total_clusters if total_clusters else 0.0
        unknown_clusters = total_clusters - fixture_candidates

        return ClusterStatistics(
            total_clusters=total_clusters,
            fixture_candidates=fixture_candidates,
            unknown_clusters=unknown_clusters,
            clusters_with_uuid=clusters_with_uuid,
            clusters_with_name=clusters_with_name,
            clusters_with_dmx=clusters_with_dmx,
            average_cluster_size=average_cluster_size,
        )


__all__ = ["ClusterAnalyzer", "ClusterStatistics"]
