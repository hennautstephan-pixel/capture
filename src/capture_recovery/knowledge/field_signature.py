from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.models import DataType


@dataclass(slots=True, frozen=True)
class FieldSignature:
    """
    Describes the expected characteristics of a semantic field.

    A FieldSignature is intentionally lightweight. It does not reference a
    particular Field instance but only the characteristics required for
    recognition.
    """

    name: str

    datatype: DataType | None = None

    dimensions: int = 1

    required: bool = True

    weight: int = 10

    description: str = ""

    def matches(
        self,
        *,
        name: str,
        datatype: DataType | None,
        dimensions: int = 1,
    ) -> bool:
        """
        Return True if a candidate field matches this signature.
        """

        if self.name.lower() != name.lower():
            return False

        if (
            self.datatype is not None
            and datatype is not None
            and self.datatype != datatype
        ):
            return False

        if self.dimensions != dimensions:
            return False

        return True

    def score(self) -> int:
        """
        Weight contributed by this field.
        """
        return self.weight

    def is_optional(self) -> bool:
        return not self.required

    def is_required(self) -> bool:
        return self.required

    def __str__(self) -> str:

        datatype = (
            self.datatype.name
            if self.datatype is not None
            else "ANY"
        )

        return (
            f"{self.name}"
            f"({datatype},"
            f"dim={self.dimensions},"
            f"weight={self.weight})"
        )