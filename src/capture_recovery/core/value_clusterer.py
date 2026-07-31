from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from capture_recovery.core.recovered_value import RecoveredValue


@dataclass(frozen=True, slots=True)
class ValueCluster:
    """Represents a cluster of recovered values.

    The cluster is intentionally immutable and acts as a lightweight container
    for values that are grouped together by a future clustering algorithm.
    """

    values: tuple[RecoveredValue, ...]
    """The recovered values belonging to this cluster."""

    @property
    def start_offset(self) -> int:
        """Return the smallest offset present in the cluster."""
        if not self.values:
            return 0
        return min(value.offset for value in self.values)

    @property
    def end_offset(self) -> int:
        """Return the largest end offset present in the cluster."""
        if not self.values:
            return 0
        return max(value.end_offset for value in self.values)

    @property
    def size(self) -> int:
        """Return the number of recovered values contained in the cluster."""
        return len(self.values)


class ValueClusterer:
    """A generic component for grouping recovered values.

    The first clustering heuristic is intentionally simple: it groups values
    solely by the proximity of their offsets in the source file.
    """

    def __init__(self, max_gap: int = 64) -> None:
        """Initialize the clusterer.

        Args:
            max_gap: The maximum allowed gap between values in a cluster.
        """
        self.max_gap = max_gap

    def cluster(self, values: Iterable[RecoveredValue]) -> list[ValueCluster]:
        """Cluster recovered values by offset proximity.

        The method converts the iterable into a list, sorts it by offset, and
        builds clusters by keeping the current cluster open when the gap between
        the next value and the current cluster end offset is within ``max_gap``.
        This first heuristic relies only on file-position proximity.
        """
        ordered_values = sorted(list(values), key=lambda value: value.offset)

        if not ordered_values:
            return []

        clusters: list[ValueCluster] = []
        current_values: list[RecoveredValue] = [ordered_values[0]]

        for value in ordered_values[1:]:
            current_cluster_end = current_values[-1].end_offset
            gap = value.offset - current_cluster_end

            if gap <= self.max_gap:
                current_values.append(value)
            else:
                clusters.append(ValueCluster(values=tuple(current_values)))
                current_values = [value]

        clusters.append(ValueCluster(values=tuple(current_values)))
        return clusters


__all__ = ["ValueCluster", "ValueClusterer"]
