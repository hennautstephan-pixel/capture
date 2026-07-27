from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .data_type import DataType


@dataclass(slots=True, order=True)
class Detection:
    """
    Detection produced by a detector.

    A Detection represents one interpreted piece of binary data extracted
    from a Capture project.
    """

    # ------------------------------------------------------------------
    # Location
    # ------------------------------------------------------------------

    offset: int
    """Start offset in the file."""

    length: int
    """Length in bytes."""

    # ------------------------------------------------------------------
    # Semantic information
    # ------------------------------------------------------------------

    datatype: DataType
    """Detected logical data type."""

    value: Any
    """Decoded value."""

    confidence: float = 1.0
    """Confidence score."""

    # ------------------------------------------------------------------
    # Origin
    # ------------------------------------------------------------------

    detector: str = ""
    """Detector name."""

    # ------------------------------------------------------------------
    # Optional information
    # ------------------------------------------------------------------

    name: str | None = None
    """Optional symbolic name."""

    description: str | None = None
    """Optional description."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Detector-specific metadata."""

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def end(self) -> int:
        """Return first byte after the detection."""
        return self.offset + self.length

    @property
    def size(self) -> int:
        """Alias for length."""
        return self.length

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    def contains(self, offset: int) -> bool:
        """Return True if offset belongs to detection."""
        return self.offset <= offset < self.end

    def overlaps(self, other: "Detection") -> bool:
        """Return True if two detections overlap."""
        return (
            self.offset < other.end
            and other.offset < self.end
        )

    def adjacent(self, other: "Detection") -> bool:
        """Return True if two detections touch each other."""
        return (
            self.end == other.offset
            or other.end == self.offset
        )

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def copy(self, **changes: Any) -> "Detection":
        """
        Return a modified copy.
        """

        values = {
            "offset": self.offset,
            "length": self.length,
            "datatype": self.datatype,
            "value": self.value,
            "confidence": self.confidence,
            "detector": self.detector,
            "name": self.name,
            "description": self.description,
            "metadata": dict(self.metadata),
        }

        values.update(changes)

        return Detection(**values)

    # ------------------------------------------------------------------
    # Magic methods
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return self.length

    def __contains__(self, offset: int) -> bool:
        return self.contains(offset)

    def __repr__(self) -> str:
        return (
            "Detection("
            f"datatype={self.datatype}, "
            f"offset=0x{self.offset:X}, "
            f"length={self.length}, "
            f"confidence={self.confidence:.2f}"
            ")"
        )