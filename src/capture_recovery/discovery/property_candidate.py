"""
Discovered property candidate.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class PropertyCandidate:
    """
    Candidate property discovered from semantic analysis.

    A PropertyCandidate represents a possible mapping between a binary
    offset and a semantic property of a Capture object.

    The confidence score is expressed between 0.0 and 1.0.
    """

    object_type: str

    property_name: str

    offset: int

    value_type: str

    confidence: float

    observations: int

    @property
    def confidence_percent(self) -> float:
        """
        Return the confidence expressed as a percentage.
        """
        return self.confidence * 100.0

    @property
    def is_high_confidence(self) -> bool:
        """
        True if confidence is at least 95%.
        """
        return self.confidence >= 0.95

    @property
    def identifier(self) -> str:
        """
        Stable identifier for this candidate.
        """
        return (
            f"{self.object_type}:"
            f"{self.property_name}:"
            f"0x{self.offset:X}"
        )