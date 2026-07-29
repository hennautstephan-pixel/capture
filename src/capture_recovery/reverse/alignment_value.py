"""
capture_recovery.reverse.alignment_value

Representation of detected alignment patterns.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class AlignmentValue:
    """
    Detected alignment information.
    """

    offset: int

    alignment: int

    score: float

    length: int


    def __post_init__(self) -> None:

        if self.offset < 0:
            raise ValueError(
                "offset must be >= 0"
            )


        if self.alignment <= 0:
            raise ValueError(
                "alignment must be > 0"
            )


        if not 0 <= self.score <= 1:
            raise ValueError(
                "score must be between 0 and 1"
            )


        if self.length < 0:
            raise ValueError(
                "length must be >= 0"
            )


    @property
    def end_offset(self) -> int:
        """
        End position of the analyzed region.
        """

        return (
            self.offset
            +
            self.length
        )


    @property
    def is_aligned(self) -> bool:
        """
        Check if offset respects alignment.
        """

        return (
            self.offset % self.alignment
            == 0
        )


    def as_dict(self) -> dict[str, object]:
        """
        Serialize value.
        """

        return {
            "offset": self.offset,
            "alignment": self.alignment,
            "score": self.score,
            "length": self.length,
        }