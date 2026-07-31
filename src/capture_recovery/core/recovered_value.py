from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RecoveredValue:
    """Represents a raw value recovered from a Capture file.

    This type is intended to be a simple, immutable container shared by
    detectors and future semantic correlators. It keeps the raw payload,
    its location in the source data, and metadata describing how it was
    extracted.
    """

    type: str
    """The nature of the recovered data, such as string, uuid, int, or float."""

    value: Any
    """The detected value itself."""

    offset: int
    """The starting offset of the value in the source file or buffer."""

    size: int
    """The size of the recovered value in bytes."""

    confidence: float = 1.0
    """The confidence score associated with the detection."""

    detector: str = ""
    """The name of the detector that produced this value."""

    source: str = ""
    """An optional source identifier such as a file name or analysis zone."""

    @property
    def end_offset(self) -> int:
        """Return the end offset of the value in the source data.

        The end offset is computed as the start offset plus the size of the
        value, and is useful for range-based comparisons.
        """
        return self.offset + self.size

    def overlaps(self, other: "RecoveredValue") -> bool:
        """Return whether this recovered value overlaps another one.

        Two values overlap when their byte ranges intersect. The comparison is
        inclusive on the start and exclusive on the end, which matches common
        file-range semantics.
        """
        return self.offset < other.end_offset and other.offset < self.end_offset


__all__ = ["RecoveredValue"]
