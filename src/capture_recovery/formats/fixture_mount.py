"""
Fixture mounting model.

Defines the relation between a fixture
and a scene structure.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FixtureMount:
    """
    Fixture attachment to a structure.
    """

    structure_id: str | None = None

    offset_x: float = 0.0

    offset_y: float = 0.0

    offset_z: float = 0.0

    rotation: tuple[float, float, float] = (
        0.0,
        0.0,
        0.0,
    )

    properties: dict = field(
        default_factory=dict,
    )