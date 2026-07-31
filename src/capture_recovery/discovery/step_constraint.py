"""
Constraint describing a constant numeric step.
"""

from __future__ import annotations

from dataclasses import dataclass

from .property_constraint import PropertyConstraint


@dataclass(frozen=True, slots=True)
class StepConstraint(PropertyConstraint):
    """
    Constraint indicating that every valid value is a multiple
    of a constant step.
    """

    step: int | float

    def __post_init__(self) -> None:

        if self.step <= 0:
            raise ValueError("step must be strictly positive")

    @property
    def name(self) -> str:
        return "StepConstraint"

    def matches(self, value: object) -> bool:

        if not isinstance(value, (int, float)):
            return False

        quotient = value / self.step

        return abs(round(quotient) - quotient) < 1e-9