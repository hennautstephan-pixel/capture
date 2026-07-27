"""
Memory region model.

A MemoryRegion represents a logical area of a Capture project file.

Regions are produced by RegionBuilder from low-level detections and are
consumed by analyzers, the Knowledge Engine and exporters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class MemoryRegion:
    """
    Logical region of a Capture file.

    Parameters
    ----------
    offset
        Starting byte offset.

    size
        Region size in bytes.

    kind
        Region type.

    confidence
        Confidence score between 0.0 and 1.0.

    source
        Name of the detector or analyzer that created this region.

    name
        Optional human-readable name.

    parent
        Parent region index (optional).

    metadata
        Additional analyzer-specific information.
    """

    offset: int
    size: int
    kind: str

    confidence: float = 1.0

    source: str = ""

    name: str | None = None

    parent: int | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def end(self) -> int:
        """
        End offset (exclusive).
        """
        return self.offset + self.size

    def contains(self, offset: int) -> bool:
        """
        Return True if the given offset belongs to the region.
        """
        return self.offset <= offset < self.end

    def overlaps(self, other: "MemoryRegion") -> bool:
        """
        Return True if two regions overlap.
        """
        return (
            self.offset < other.end
            and other.offset < self.end
        )

    def adjacent(self, other: "MemoryRegion") -> bool:
        """
        Return True if two regions touch each other.
        """
        return (
            self.end == other.offset
            or other.end == self.offset
        )

    def merge(self, other: "MemoryRegion") -> "MemoryRegion":
        """
        Merge two adjacent regions.

        Raises
        ------
        ValueError
            If the regions are not mergeable.
        """

        if self.kind != other.kind:
            raise ValueError(
                "Cannot merge regions of different kinds."
            )

        if not self.adjacent(other):
            raise ValueError(
                "Regions are not adjacent."
            )

        start = min(self.offset, other.offset)
        end = max(self.end, other.end)

        return MemoryRegion(
            offset=start,
            size=end - start,
            kind=self.kind,
            confidence=max(
                self.confidence,
                other.confidence,
            ),
            source=self.source or other.source,
            metadata={
                **self.metadata,
                **other.metadata,
            },
        )

    def __len__(self) -> int:
        return self.size

    def __contains__(self, offset: int) -> bool:
        return self.contains(offset)

    def __lt__(self, other: "MemoryRegion") -> bool:
        return self.offset < other.offset

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"offset=0x{self.offset:X}, "
            f"size={self.size}, "
            f"kind='{self.kind}')"
        )