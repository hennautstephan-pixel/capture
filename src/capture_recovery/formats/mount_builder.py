"""
Fixture mount builder.

Builds fixture attachment data from
semantic fixture objects.
"""

from __future__ import annotations

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from .fixture_mount import (
    FixtureMount,
)


class MountBuilder:
    """
    Build fixture mounts.
    """

    def build(
        self,
        fixture: SemanticObject,
    ) -> FixtureMount:
        """
        Convert mount data into
        FixtureMount.
        """

        mount = fixture.properties.get(
            "mount",
            {},
        )

        if not isinstance(
            mount,
            dict,
        ):
            mount = {}

        rotation = mount.get(
            "rotation",
            (
                0.0,
                0.0,
                0.0,
            ),
        )

        return FixtureMount(
            structure_id=mount.get(
                "structure_id",
            ),

            offset_x=mount.get(
                "offset_x",
                0.0,
            ),

            offset_y=mount.get(
                "offset_y",
                0.0,
            ),

            offset_z=mount.get(
                "offset_z",
                0.0,
            ),

            rotation=(
                rotation[0],
                rotation[1],
                rotation[2],
            ),

            properties=fixture.properties.copy(),
        )

    def can_build(
        self,
        fixture: SemanticObject,
    ) -> bool:
        """
        Check fixture type.
        """

        return (
            fixture.object_type
            == "Fixture"
        )