"""
World position model.

Represents the absolute position
of an object in the scene.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class WorldPosition:
    """
    Absolute 3D world position.
    """

    x: float = 0.0

    y: float = 0.0

    z: float = 0.0

    pan: float = 0.0

    tilt: float = 0.0

    roll: float = 0.0