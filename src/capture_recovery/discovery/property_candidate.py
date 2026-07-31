"""
Discovered property candidate.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .property_constraint import PropertyConstraint
from .value_type import ValueType


@dataclass(frozen=True, slots=True)
class PropertyCandidate:
    """
    Candidate describing an inferred property.
    """

    #: Type of object (Fixture, Universe, Group, ...)
    object_type: str

    #: Semantic property name
    property_name: str

    #: Binary offset within the structure
    offset: int

    #: Inferred value type
    value_type: ValueType

    #: Confidence score in the range [0.0, 1.0]
    confidence: float

    #: Number of observations used for the inference
    observations: int

    #: Additional semantic constraints inferred for this property.
    #: Empty for existing correlators to preserve backward compatibility.
    constraints: tuple[PropertyConstraint, ...] = field(default_factory=tuple)

    @property
    def confidence_percent(self) -> float:
        """
        Confidence expressed as a percentage.
        """
        return self.confidence * 100.0