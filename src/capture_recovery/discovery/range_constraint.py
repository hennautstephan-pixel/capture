"""
Constraint describing a numeric range.
"""

from __future__ import annotations

from dataclasses import dataclass

from .property_constraint import PropertyConstraint


@dataclass(frozen=True, slots=True)
class RangeConstraint(PropertyConstraint):
    """
    Constraint indicating that a property must remain inside
    a discovered numeric interval.
    """

    minimum: int | float
    maximum: int | float

    def __post_init__(self) -> None:
        if self.minimum > self.maximum:
            raise ValueError(
                "minimum must be less than or equal to maximum"
            )

    @property
    def name(self) -> str:
        return "RangeConstraint"

    def matches(self, value: object) -> bool:

        if not isinstance(value, (int, float)):
            return False

        return self.minimum <= value <= self.maximum