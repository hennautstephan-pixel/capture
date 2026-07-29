from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from capture_recovery.binary.string_scanner import ExtractedString


@dataclass(slots=True)
class Segment:
    offset: int
    length: int

    kind: str = "unknown"

    confidence: float = 0.0

    entropy: float | None = None

    signature: str |None = None

    strings: list[ExtractedString] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    children: list["Segment"] = field(default_factory=list)

    @property
    def end(self) -> int:
        return self.offset + self.length

    @property
    def size(self) -> int:
        return self.length

    def __len__(self) -> int:
        return self.length

    def contains(self, offset: int) -> bool:
        return self.offset <= offset < self.end

    def overlaps(self, other: "Segment") -> bool:
        return (
            self.offset < other.end
            and other.offset < self.end
        )

    def add_child(self, child: "Segment") -> None:
        self.children.append(child)

    def to_dict(self) -> dict[str, Any]:
        return {
            "offset": self.offset,
            "length": self.length,
            "kind": self.kind,
            "confidence": self.confidence,
            "entropy": self.entropy,
            "signature": self.signature,
            "strings": [
                {
                    "offset": s.offset,
                    "encoding": s.encoding,
                    "text": s.text,
                }
                for s in self.strings
            ],
            "metadata": dict(self.metadata),
            "children": [c.to_dict() for c in self.children],
        }