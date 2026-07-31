"""
Benchmark statistics.
"""

from __future__ import annotations

from collections.abc import Iterable

from .benchmark_result import BenchmarkResult


class BenchmarkStatistics:
    """
    Aggregates several BenchmarkResult instances.
    """

    def __init__(
        self,
        results: Iterable[BenchmarkResult] = (),
    ) -> None:

        self._results = list(results)

    @property
    def results(self) -> tuple[BenchmarkResult, ...]:
        return tuple(self._results)

    def add(
        self,
        result: BenchmarkResult,
    ) -> None:

        self._results.append(result)

    def merge(
        self,
        other: "BenchmarkStatistics",
    ) -> None:
        """
        Merge another BenchmarkStatistics into this one.
        """

        self._results.extend(other.results)

    def to_dict(self) -> dict[str, object]:
        """
        Serialize statistics as a dictionary.
        """

        return {
            "project_count": self.project_count,
            "total_file_size": self.total_file_size,
            "average_file_size": self.average_file_size,
            "total_objects": self.total_objects,
            "recovered_objects": self.recovered_objects,
            "unknown_objects": self.unknown_objects,
            "recovery_rate": self.recovery_rate,
            "total_properties": self.total_properties,
            "total_candidates": self.total_candidates,
            "average_confidence": self.average_confidence,
            "minimum_confidence": self.minimum_confidence,
            "maximum_confidence": self.maximum_confidence,
            "total_conflicts": self.total_conflicts,
            "total_unknown_signatures": (
                self.total_unknown_signatures
            ),
            "total_duration": self.total_duration,
            "average_duration": self.average_duration,
        }

    @property
    def project_count(self) -> int:
        return len(self._results)

    @property
    def total_file_size(self) -> int:
        return sum(
            r.file_size
            for r in self._results
        )

    @property
    def average_file_size(self) -> float:

        if not self._results:
            return 0.0

        return (
            self.total_file_size
            / len(self._results)
        )

    @property
    def total_objects(self) -> int:
        return sum(
            r.object_count
            for r in self._results
        )

    @property
    def recovered_objects(self) -> int:
        return sum(
            r.recovered_objects
            for r in self._results
        )

    @property
    def unknown_objects(self) -> int:
        return sum(
            r.unknown_objects
            for r in self._results
        )

    @property
    def recovery_rate(self) -> float:

        if self.total_objects == 0:
            return 0.0

        return (
            self.recovered_objects
            / self.total_objects
        )

    @property
    def total_properties(self) -> int:
        return sum(
            r.property_count
            for r in self._results
        )

    @property
    def total_candidates(self) -> int:
        return sum(
            r.candidate_count
            for r in self._results
        )

    @property
    def average_confidence(self) -> float:

        if not self._results:
            return 0.0

        return (
            sum(
                r.average_confidence
                for r in self._results
            )
            / len(self._results)
        )

    @property
    def minimum_confidence(self) -> float:

        if not self._results:
            return 0.0

        return min(
            r.minimum_confidence
            for r in self._results
        )

    @property
    def maximum_confidence(self) -> float:

        if not self._results:
            return 0.0

        return max(
            r.maximum_confidence
            for r in self._results
        )

    @property
    def total_conflicts(self) -> int:
        return sum(
            r.conflict_count
            for r in self._results
        )

    @property
    def total_unknown_signatures(self) -> int:
        return sum(
            r.unknown_signature_count
            for r in self._results
        )

    @property
    def total_duration(self) -> float:
        return sum(
            r.duration_seconds
            for r in self._results
        )

    @property
    def average_duration(self) -> float:

        if not self._results:
            return 0.0

        return (
            self.total_duration
            / len(self._results)
        )