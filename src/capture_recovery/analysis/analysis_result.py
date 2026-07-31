"""
Analysis result.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from capture_recovery.discovery import PropertyCandidate


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """
    Result of analysing a single Capture project.
    """

    filename: str

    file_size: int

    object_count: int

    property_count: int

    candidate_count: int

    average_confidence: float

    minimum_confidence: float

    maximum_confidence: float

    unknown_objects: int

    unknown_signatures: int

    conflict_count: int

    duration_seconds: float

    candidates: tuple[PropertyCandidate, ...] = field(
        default_factory=tuple
    )

    @property
    def recovery_rate(self) -> float:

        if self.object_count == 0:
            return 0.0

        return (
            self.object_count - self.unknown_objects
        ) / self.object_count

    @property
    def recovered_objects(self) -> int:

        return (
            self.object_count
            - self.unknown_objects
        )

    @property
    def analysed(self) -> bool:

        return self.duration_seconds >= 0.0