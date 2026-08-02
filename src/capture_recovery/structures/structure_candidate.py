from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .cluster import Cluster


@dataclass(slots=True)
class StructureCandidate:
    """
    Candidate structure inferred from a Cluster.

    A StructureCandidate represents an intermediate reconstruction step
    before semantic validation.

    DetectionIndex
            │
            ▼
        Cluster
            │
            ▼
    StructureCandidate
            │
            ▼
        Structure
    """

    cluster: Cluster

    estimated_type: str = "Unknown"

    confidence: float = 0.0

    score: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Geometry
    # ---------------------------------------------------------

    @property
    def offset(self) -> int:
        return self.cluster.start

    @property
    def length(self) -> int:
        return self.cluster.span

    @property
    def end(self) -> int:
        return self.cluster.end

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @property
    def field_count(self) -> int:
        return self.cluster.detection_count

    @property
    def density(self) -> float:
        """
        Ratio between occupied bytes and total span.
        """

        if self.length == 0:
            return 0.0

        occupied = sum(
            d.length
            for d in self.cluster
        )

        return occupied / self.length

    @property
    def average_confidence(self) -> float:
        return self.cluster.confidence

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
    # Magic methods
    # ---------------------------------------------------------

    def __len__(self) -> int:
        return self.field_count

    def __iter__(self):
        return iter(
            self.cluster,
        )

    def __repr__(self) -> str:
        return (
            "StructureCandidate("
            f"type={self.estimated_type}, "
            f"offset=0x{self.offset:X}, "
            f"length={self.length}, "
            f"fields={self.field_count}, "
            f"score={self.score:.2f})"
        )