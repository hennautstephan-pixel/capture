"""
Fixture position builder.

Builds spatial fixture positions from
recovered semantic objects.
"""

from __future__ import annotations

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from .fixture_position import (
    FixturePosition,
)


class PositionBuilder:
    """
    Build fixture positions.
    """

    def build(
        self,
        fixture: SemanticObject,
    ) -> FixturePosition:
        """
        Convert fixture placement data.
        """

        position = fixture.properties.get(
            "position",
            {},
        )

        rotation = fixture.properties.get(
            "rotation",
            {},
        )

        # Legacy semantic format:
        # position = (x, y, z)
        if isinstance(position, tuple):
            position = {
                "x": position[0],
                "y": position[1],
                "z": position[2],
            }

        # Legacy semantic format:
        # rotation = (pan, tilt, roll)
        if isinstance(rotation, tuple):
            rotation = {
                "pan": rotation[0],
                "tilt": rotation[1],
                "roll": rotation[2],
            }

        return FixturePosition(
            x=position.get(
                "x",
                0.0,
            ),

            y=position.get(
                "y",
                0.0,
            ),

            z=position.get(
                "z",
                0.0,
            ),

            pan=rotation.get(
                "pan",
                0.0,
            ),

            tilt=rotation.get(
                "tilt",
                0.0,
            ),

            roll=rotation.get(
                "roll",
                0.0,
            ),

            properties=fixture.properties.copy(),
        )

    def can_build(
        self,
        fixture: SemanticObject,
    ) -> bool:
        """
        Check fixture object.
        """

        return (
            fixture.object_type
            == "Fixture"
        )