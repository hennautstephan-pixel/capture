"""
Object relations.

Represents semantic relationships
between recovered Capture objects.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ObjectRelation:
    """
    Relationship between two recovered objects.
    """

    source: str

    target: str

    relation_type: str

    properties: dict = field(
        default_factory=dict,
    )