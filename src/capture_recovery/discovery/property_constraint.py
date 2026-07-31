"""
Base class for semantic property constraints.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PropertyConstraint:
    """
    Base class for all semantic constraints inferred during discovery.

    Examples of derived constraints include:

    - EnumConstraint
    - RangeConstraint
    - DefaultValueConstraint
    - StringLengthConstraint
    """

    @property
    def name(self) -> str:
        """
        Human-readable constraint name.
        """
        return self.__class__.__name__