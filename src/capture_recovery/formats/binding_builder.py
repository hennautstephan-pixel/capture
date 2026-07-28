"""
Structure binding builder.

Creates inverse relations between
structures and mounted fixtures.
"""

from __future__ import annotations

from .capture_project import (
    CaptureProject,
)

from .structure_binding import (
    StructureBinding,
)


class BindingBuilder:
    """
    Build structure fixture bindings.
    """

    def build(
        self,
        project: CaptureProject,
    ) -> list[StructureBinding]:
        """
        Create bindings from fixture mounts.
        """

        bindings: dict[str, StructureBinding] = {}

        for fixture in project.fixtures:

            mount = fixture.mount

            if mount.structure_id is None:
                continue

            if mount.structure_id not in bindings:

                bindings[mount.structure_id] = (
                    StructureBinding(
                        structure_id=(
                            mount.structure_id
                        ),
                    )
                )

            bindings[
                mount.structure_id
            ].add_fixture(
                fixture.name,
            )

        return list(
            bindings.values(),
        )