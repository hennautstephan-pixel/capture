from __future__ import annotations

from dataclasses import dataclass, field

from .field import Field


@dataclass(slots=True)
class Structure:
    """
    High-level binary structure reconstructed from detections.
    """

    name: str

    offset: int

    length: int

    confidence: float = 1.0

    fields: list[Field] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    @property
    def end(self) -> int:
        return self.offset + self.length

    def add(self, field: Field) -> None:
        self.fields.append(field)

    def sort(self) -> None:
        self.fields.sort(key=lambda f: f.offset)

    def contains(self, offset: int) -> bool:
        return self.offset <= offset < self.end

    def __len__(self) -> int:
        return self.length

    def __iter__(self):
        return iter(self.fields)

    def __repr__(self) -> str:
        return (
            f"Structure("
            f"name={self.name!r}, "
            f"offset=0x{self.offset:X}, "
            f"length={self.length}, "
            f"fields={len(self.fields)})"
        )