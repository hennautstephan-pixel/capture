"""
Benchmark result.

Represents the metrics collected while analysing a single Capture project.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    """
    Benchmark result for a single project.
    """

    #: Project filename.
    filename: str

    #: File size in bytes.
    file_size: int

    #: Number of binary objects detected.
    object_count: int

    #: Number of objects successfully reconstructed.
    recovered_objects: int

    #: Number of objects that could not be reconstructed.
    unknown_objects: int

    #: Number of semantic properties analysed.
    property_count: int

    #: Number of PropertyCandidate instances produced.
    candidate_count: int

    #: Average confidence of all discovered candidates.
    average_confidence: float

    #: Lowest confidence encountered.
    minimum_confidence: float

    #: Highest confidence encountered.
    maximum_confidence: float

    #: Number of constraint conflicts.
    conflict_count: int

    #: Number of unknown binary signatures.
    unknown_signature_count: int

    #: Analysis duration in seconds.
    duration_seconds: float

    @property
    def recovery_rate(self) -> float:
        """
        Returns the reconstruction rate.

        Value is between 0.0 and 1.0.
        """

        if self.object_count == 0:
            return 0.0

        return self.recovered_objects / self.object_count

    @property
    def unknown_rate(self) -> float:
        """
        Returns the unknown object rate.

        Value is between 0.0 and 1.0.
        """

        if self.object_count == 0:
            return 0.0

        return self.unknown_objects / self.object_count

    @property
    def analysed(self) -> bool:
        """
        Indicates whether the benchmark completed successfully.
        """

        return self.duration_seconds >= 0.0