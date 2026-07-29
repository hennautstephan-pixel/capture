"""
capture_recovery.reverse.entropy_value

Representation of entropy analysis results.
"""

from __future__ import annotations

from dataclasses import dataclass



@dataclass(
    frozen=True,
    slots=True,
)
class EntropyValue:
    """
    Entropy measurement result.

    Attributes
    ----------
    offset:
        Start offset.

    entropy:
        Shannon entropy value (0-8 bits).

    length:
        Size of analyzed block.

    score:
        Normalized entropy score (0-1).
    """

    offset: int

    entropy: float

    length: int

    score: float



    def __post_init__(self) -> None:

        if self.offset < 0:
            raise ValueError(
                "offset must be >= 0"
            )


        if self.length < 0:
            raise ValueError(
                "length must be >= 0"
            )


        if not 0 <= self.entropy <= 8:
            raise ValueError(
                "entropy must be between 0 and 8"
            )


        if not 0 <= self.score <= 1:
            raise ValueError(
                "score must be between 0 and 1"
            )



    @property
    def is_high_entropy(self) -> bool:
        """
        True when entropy is above 6 bits.
        """

        return self.entropy >= 6.0



    @property
    def end_offset(self) -> int:
        """
        End position.
        """

        return (
            self.offset
            +
            self.length
        )



    def as_dict(self) -> dict[str, object]:
        """
        Serialize result.
        """

        return {
            "offset": self.offset,
            "entropy": self.entropy,
            "score": self.score,
            "length": self.length,
        }