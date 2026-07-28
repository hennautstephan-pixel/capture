"""
Spatial transformation.

Applies structure transformations
to local fixture coordinates.
"""

from __future__ import annotations

from .rotation_math import (
    RotationMath,
)

from .world_position import (
    WorldPosition,
)


class SpatialTransform:
    """
    Transform local coordinates into
    world coordinates.
    """

    def transform_position(
        self,
        local: tuple[float, float, float],
        origin: tuple[float, float, float],
        rotation: tuple[float, float, float],
    ) -> WorldPosition:
        """
        Apply rotation then translation.
        """

        rotated = RotationMath.rotate_xyz(
            local,
            rotation,
        )

        return WorldPosition(
            x=origin[0] + rotated[0],

            y=origin[1] + rotated[1],

            z=origin[2] + rotated[2],
        )