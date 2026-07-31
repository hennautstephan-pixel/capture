"""
Constraint describing a valid bitmask.
"""

from __future__ import annotations

from dataclasses import dataclass

from .property_constraint import PropertyConstraint


@dataclass(frozen=True, slots=True)
class BitmaskConstraint(PropertyConstraint):
    """
    Constraint indicating that only bits present in the discovered
    mask may be set.
    """

    mask: int

    def __post_init__(self) -> None:

        if self.mask < 0:
            raise ValueError("mask must be non-negative")

    @property
    def name(self) -> str:
        return "BitmaskConstraint"

    def matches(self, value: object) -> bool:

        if not isinstance(value, int):
            return False

        return (value & ~self.mask) == 0