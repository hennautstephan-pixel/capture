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

    @property
    def score(self) -> float:
        """
        Reconstruction score.

        Falls back to confidence when no explicit score
        has been computed.
        """

        return float(
            self.metadata.get(
                "score",
                self.confidence,
            )
        )

    @property
    def estimated_type(self) -> str:
        """
        Best inferred semantic type.

        Falls back to the structure name.
        """

        return str(
            self.metadata.get(
                "estimated_type",
                self.name,
            )
        )

    def add(
        self,
        field: Field,
    ) -> None:

        self.fields.append(field)

    def sort(self) -> None:

        self.fields.sort(
            key=lambda f: f.offset,
        )

    def contains(
        self,
        offset: int,
    ) -> bool:

        return (
            self.offset
            <= offset
            < self.end
        )

    def __len__(self) -> int:

        return self.length

    def __iter__(self):

        return iter(
            self.fields,
        )

    def __repr__(self) -> str:

        return (
            "Structure("
            f"name={self.name!r}, "
            f"offset=0x{self.offset:X}, "
            f"length={self.length}, "
            f"score={self.score:.2f}, "
            f"fields={len(self.fields)})"
        )