from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CaptureField:
    """
    A field experimentally identified inside the Capture binary format.

    Every field stored here must come from observations performed on the
    sample corpus.
    """

    name: str

    offset: int

    size: int

    confidence: float

    metadata: dict[str, Any] = field(default_factory=dict)


class CaptureFormat:
    """
    Experimental specification of the Capture binary format.

    This class contains only demonstrated knowledge extracted from
    the project corpus.
    """

    def __init__(self) -> None:

        self._fields: dict[str, CaptureField] = {}

    def add_field(
        self,
        field: CaptureField,
    ) -> None:

        self._fields[field.name] = field

    def get(
        self,
        name: str,
    ) -> CaptureField | None:

        return self._fields.get(name)

    def all_fields(
        self,
    ) -> tuple[CaptureField, ...]:

        return tuple(
            sorted(
                self._fields.values(),
                key=lambda f: f.offset,
            )
        )

    def statistics(
        self,
    ) -> dict[str, int | float]:

        if not self._fields:
            return {
                "field_count": 0,
                "average_confidence": 0.0,
            }

        average = (
            sum(
                field.confidence
                for field in self._fields.values()
            )
            / len(self._fields)
        )

        return {
            "field_count": len(self._fields),
            "average_confidence": average,
        }

    @classmethod
    def default(
        cls,
    ) -> "CaptureFormat":

        fmt = cls()

        #
        # Observations experimentally confirmed
        # on the current sample corpus.
        #

        fmt.add_field(
            CaptureField(
                name="Project",
                offset=0x0004,
                size=8,
                confidence=1.0,
                metadata={
                    "encoding": "ascii",
                    "value": "Project",
                    "status": "confirmed",
                },
            )
        )

        fmt.add_field(
            CaptureField(
                name="SoftwareVersion",
                offset=0x0014,
                size=16,
                confidence=1.0,
                metadata={
                    "encoding": "ascii",
                    "value": "SoftwareVersion",
                    "status": "confirmed",
                },
            )
        )

        return fmt


__all__ = [
    "CaptureField",
    "CaptureFormat",
]