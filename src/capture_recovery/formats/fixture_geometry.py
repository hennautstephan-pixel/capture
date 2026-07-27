"""
Fixture geometry model.

Contains physical placement and orientation
information for lighting fixtures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class FixtureGeometry:
    """
    Physical geometry of a lighting fixture.
    """

    position: tuple[float, float, float] = (
        0.0,
        0.0,
        0.0,
    )

    rotation: tuple[float, float, float] = (
        0.0,
        0.0,
        0.0,
    )

    scale: tuple[float, float, float] = (
        1.0,
        1.0,
        1.0,
    )

    height: float = 0.0

    focus_point: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def x(self) -> float:
        return self.position[0]

    @property
    def y(self) -> float:
        return self.position[1]

    @property
    def z(self) -> float:
        return self.position[2]

    @property
    def pan(self) -> float:
        return self.rotation[0]

    @property
    def tilt(self) -> float:
        return self.rotation[1]

    @property
    def roll(self) -> float:
        return self.rotation[2]

    def translated(
        self,
        x: float,
        y: float,
        z: float,
    ) -> FixtureGeometry:
        """
        Return a translated copy.
        """

        return FixtureGeometry(
            position=(
                x,
                y,
                z,
            ),
            rotation=self.rotation,
            scale=self.scale,
            height=self.height,
            focus_point=self.focus_point,
            metadata=self.metadata.copy(),
        )

    def rotated(
        self,
        pan: float,
        tilt: float,
        roll: float = 0.0,
    ) -> FixtureGeometry:
        """
        Return a rotated copy.
        """

        return FixtureGeometry(
            position=self.position,
            rotation=(
                pan,
                tilt,
                roll,
            ),
            scale=self.scale,
            height=self.height,
            focus_point=self.focus_point,
            metadata=self.metadata.copy(),
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert geometry to serializable data.
        """

        return {
            "position": self.position,
            "rotation": self.rotation,
            "scale": self.scale,
            "height": self.height,
            "focus_point": self.focus_point,
            "metadata": self.metadata,
        }