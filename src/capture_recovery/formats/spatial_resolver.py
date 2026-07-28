"""
Spatial resolver.

Computes final fixture world positions
from structures, mounts and transforms.
"""

from __future__ import annotations

from .capture_project import (
    CaptureFixture,
    CaptureProject,
)

from .spatial_transform import (
    SpatialTransform,
)

from .world_position import (
    WorldPosition,
)


class SpatialResolver:
    """
    Resolve world positions.
    """

    def __init__(
        self,
        transform: SpatialTransform | None = None,
    ) -> None:

        self.transform = (
            transform
            or SpatialTransform()
        )

    def resolve_fixture(
        self,
        fixture: CaptureFixture,
        project: CaptureProject,
    ) -> WorldPosition:
        """
        Compute absolute fixture position.
        """

        mount = fixture.mount

        if mount.structure_id is None:

            return WorldPosition(
                x=fixture.position.x,
                y=fixture.position.y,
                z=fixture.position.z,
                pan=fixture.position.pan,
                tilt=fixture.position.tilt,
                roll=fixture.position.roll,
            )

        structure = self._find_structure(
            mount.structure_id,
            project,
        )

        if structure is None:

            return WorldPosition(
                x=fixture.position.x,
                y=fixture.position.y,
                z=fixture.position.z,
                pan=fixture.position.pan,
                tilt=fixture.position.tilt,
                roll=fixture.position.roll,
            )

        local_position = (
            mount.offset_x,
            mount.offset_y,
            mount.offset_z,
        )

        world = (
            self.transform.transform_position(
                local_position,

                structure.position,

                structure.rotation,
            )
        )

        world.pan = fixture.position.pan
        world.tilt = fixture.position.tilt
        world.roll = fixture.position.roll

        return world

    def resolve_project(
        self,
        project: CaptureProject,
    ) -> dict[str, WorldPosition]:
        """
        Resolve all fixture positions.
        """

        result = {}

        for fixture in project.fixtures:

            result[fixture.name] = (
                self.resolve_fixture(
                    fixture,
                    project,
                )
            )

        return result

    def _find_structure(
        self,
        structure_id: str,
        project: CaptureProject,
    ):

        for structure in project.structures:

            if structure.name == structure_id:

                return structure

        return None