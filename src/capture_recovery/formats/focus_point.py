"""
Fixture focus point model.

Contains the 3D target point
of a fixture.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FocusPoint:
    """
    3D focus target.
    """

    x: float = 0.0

    y: float = 0.0

    z: float = 0.0

    properties: dict = field(
        default_factory=dict,
    )