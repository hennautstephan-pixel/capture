"""
Constraint describing an enumerated set of allowed values.
"""

from __future__ import annotations

from dataclasses import dataclass

from .property_constraint import PropertyConstraint


@dataclass(frozen=True, slots=True)
class EnumConstraint(PropertyConstraint):
    """
    Constraint indicating that a property may only take one of a fixed
    set of values discovered during analysis.
    """

    values: tuple[object, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", tuple(dict.fromkeys(self.values)))

    @property
    def name(self) -> str:
        return "EnumConstraint"

    def matches(self, value: object) -> bool:
        return value in self.values