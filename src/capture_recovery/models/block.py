from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Block:
    """Représente un bloc logique identifié dans un fichier."""

    name: str
    offset: int
    length: int
    confidence: float = 1.0
    metadata: dict[str, object] = field(default_factory=dict)

    @property
    def end(self) -> int:
        """Premier octet après le bloc."""
        return self.offset + self.length

    def __repr__(self) -> str:
        return (
            f"Block("
            f"name={self.name!r}, "
            f"offset={self.offset}, "
            f"length={self.length}, "
            f"confidence={self.confidence:.2f}"
            f")"
        )