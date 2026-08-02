from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from capture_recovery.structures import StructureCandidate


@dataclass(slots=True)
class Hypothesis:
    """
    Semantic hypothesis produced from a StructureCandidate.

    A hypothesis represents one possible interpretation of a binary
    structure.

    It contains no inference logic; it is only a data model.
    """

    object_type: str

    confidence: float

    candidate: StructureCandidate

    source: str = "Unknown"

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Geometry
    # ---------------------------------------------------------

    @property
    def offset(self) -> int:
        return self.candidate.offset

    @property
    def length(self) -> int:
        return self.candidate.length

    @property
    def end(self) -> int:
        return self.candidate.end

    # ---------------------------------------------------------
    # Candidate information
    # ---------------------------------------------------------

    @property
    def field_count(self) -> int:
        return self.candidate.field_count

    @property
    def score(self) -> float:
        return self.candidate.score

    @property
    def density(self) -> float:
        return self.candidate.density

    # ---------------------------------------------------------
    # Metadata helpers
    # ---------------------------------------------------------

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.metadata.get(
            key,
            default,
        )

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value

    # ---------------------------------------------------------
    # Ordering
    # ---------------------------------------------------------

    def __lt__(
        self,
        other: "Hypothesis",
    ) -> bool:

        return self.confidence < other.confidence

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "Hypothesis("
            f"type={self.object_type!r}, "
            f"confidence={self.confidence:.2f}, "
            f"offset=0x{self.offset:X}, "
            f"fields={self.field_count})"
        )