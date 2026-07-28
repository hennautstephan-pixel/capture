"""
Fixture position models.

Contains spatial placement information
for Capture fixtures.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FixturePosition:
    """
    3D fixture position.

    Coordinates are expressed in Capture
    scene units.
    """

    x: float = 0.0

    y: float = 0.0

    z: float = 0.0

    pan: float = 0.0

    tilt: float = 0.0

    roll: float = 0.0

    properties: dict = field(
        default_factory=dict,
    )