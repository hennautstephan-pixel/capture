"""
capture_recovery.parser.segment

Representation of a binary segment.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Segment:
    """
    Represents a contiguous region of binary data.
    """

    offset: int
    length: int

    kind: str = "unknown"

    confidence: float = 0.0

    label: str | None = None

    metadata: dict[str, object] = field(default_factory=dict)

    children: list["Segment"] = field(default_factory=list)

    @property
    def end(self) -> int:
        return self.offset + self.length

    def contains(self, offset: int) -> bool:
        return self.offset <= offset < self.end

    def overlaps(self, other: "Segment") -> bool:
        return (
            self.offset < other.end
            and other.offset < self.end
        )

    def add_child(self, child: "Segment") -> None:
        self.children.append(child)

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        return (
            f"Segment("
            f"offset={self.offset}, "
            f"length={self.length}, "
            f"kind={self.kind!r}, "
            f"confidence={self.confidence:.2f})"
        )