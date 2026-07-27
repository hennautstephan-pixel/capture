from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Detection:
    """Résultat produit par un détecteur."""

    datatype: str
    offset: int
    length: int
    value: object
    confidence: float

    @property
    def end(self) -> int:
        """Offset du premier octet après la détection."""
        return self.offset + self.length

    def __repr__(self) -> str:
        return (
            f"Detection("
            f"datatype={self.datatype!r}, "
            f"offset={self.offset}, "
            f"length={self.length}, "
            f"value={self.value!r}, "
            f"confidence={self.confidence:.2f}"
            f")"
        )