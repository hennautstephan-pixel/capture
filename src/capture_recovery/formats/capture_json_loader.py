"""
Capture JSON loader.

Loads CaptureProject models from
JSON-compatible dictionaries.
"""

from __future__ import annotations

import json
from pathlib import Path

from .capture_group import (
    CaptureGroup,
)

from .capture_patch import (
    CapturePatch,
    PatchEntry,
)

from .capture_project import (
    CaptureCue,
    CaptureFixture,
    CaptureProject,
    CaptureUniverse,
)

from .fixture_position import (
    FixturePosition,
)

from .focus_point import (
    FocusPoint,
)

from .fixture_mount import (
    FixtureMount,
)

from .structure_binding import (
    StructureBinding,
)

from .scene_structure import (
    SceneStructure,
)


class CaptureJsonLoader:
    """
    Load Capture projects from JSON.
    """

    def from_dict(
        self,
        data: dict,
    ) -> CaptureProject:
        """
        Convert dictionary into
        CaptureProject.
        """

        project_data = data.get(
            "project",
            data,
        )

        project = CaptureProject(
            name=project_data.get(
                "name",
                "Recovered Capture",
            ),
        )

        # Fixtures

        for fixture_data in data.get(
            "fixtures",
            [],
        ):

            position_data = fixture_data.get(
                "position",
                {},
            )

            position = FixturePosition(
                x=position_data.get(
                    "x",
                    0.0,
                ),

                y=position_data.get(
                    "y",
                    0.0,
                ),

                z=position_data.get(
                    "z",
                    0.0,
                ),

                pan=position_data.get(
                    "pan",
                    0.0,
                ),

                tilt=position_data.get(
                    "tilt",
                    0.0,
                ),

                roll=position_data.get(
                    "roll",
                    0.0,
                ),
            )

            focus_data = fixture_data.get(
                "focus_point",
                {},
            )

            focus = FocusPoint(
                x=focus_data.get(
                    "x",
                    0.0,
                ),

                y=focus_data.get(
                    "y",
                    0.0,
                ),

                z=focus_data.get(
                    "z",
                    0.0,
                ),
            )

            mount_data = fixture_data.get(
                "mount",
                {},
            )

            mount_rotation = mount_data.get(
                "rotation",
                [
                    0.0,
                    0.0,
                    0.0,
                ],
            )

            mount = FixtureMount(
                structure_id=mount_data.get(
                    "structure_id",
                ),

                offset_x=mount_data.get(
                    "offset_x",
                    0.0,
                ),

                offset_y=mount_data.get(
                    "offset_y",
                    0.0,
                ),

                offset_z=mount_data.get(
                    "offset_z",
                    0.0,
                ),

                rotation=(
                    mount_rotation[0],
                    mount_rotation[1],
                    mount_rotation[2],
                ),

                properties=mount_data.get(
                    "properties",
                    {},
                ),
            )

            project.add_fixture(
                CaptureFixture(
                    name=fixture_data.get(
                        "name",
                        "",
                    ),

                    universe=fixture_data.get(
                        "universe",
                        0,
                    ),

                    address=fixture_data.get(
                        "address",
                        0,
                    ),

                    manufacturer=fixture_data.get(
                        "manufacturer",
                    ),

                    model=fixture_data.get(
                        "model",
                    ),

                    mode=fixture_data.get(
                        "mode",
                    ),

                    position=position,

                    focus_point=focus,

                    mount=mount,

                    properties=fixture_data.get(
                        "properties",
                        {},
                    ),
                )
            )

        # Universes

        for universe_data in data.get(
            "universes",
            [],
        ):

            project.add_universe(
                CaptureUniverse(
                    name=universe_data.get(
                        "name",
                        "",
                    ),

                    universe=universe_data.get(
                        "universe",
                        0,
                    ),

                    protocol=universe_data.get(
                        "protocol",
                    ),

                    properties=universe_data.get(
                        "properties",
                        {},
                    ),
                )
            )

        # Cues

        for cue_data in data.get(
            "cues",
            [],
        ):

            project.add_cue(
                CaptureCue(
                    name=cue_data.get(
                        "name",
                        "",
                    ),

                    number=cue_data.get(
                        "number",
                        0,
                    ),

                    properties=cue_data.get(
                        "properties",
                        {},
                    ),
                )
            )

        # Patch

        patch = CapturePatch()

        for entry_data in data.get(
            "patch",
            {},
        ).get(
            "entries",
            [],
        ):

            patch.add(
                PatchEntry(
                    fixture=entry_data.get(
                        "fixture",
                        "",
                    ),

                    universe=entry_data.get(
                        "universe",
                        0,
                    ),

                    address=entry_data.get(
                        "address",
                        0,
                    ),

                    mode=entry_data.get(
                        "mode",
                    ),

                    channels=entry_data.get(
                        "channels",
                        0,
                    ),

                    properties=entry_data.get(
                        "properties",
                        {},
                    ),
                )
            )

        project.patch = patch

        # Groups

        for group_data in data.get(
            "groups",
            [],
        ):

            project.add_group(
                CaptureGroup(
                    name=group_data.get(
                        "name",
                        "",
                    ),

                    fixtures=group_data.get(
                        "fixtures",
                        [],
                    ),

                    properties=group_data.get(
                        "properties",
                        {},
                    ),
                )
            )

        # Structures

        for structure_data in data.get(
            "structures",
            [],
        ):

            position = structure_data.get(
                "position",
                [
                    0.0,
                    0.0,
                    0.0,
                ],
            )

            rotation = structure_data.get(
                "rotation",
                [
                    0.0,
                    0.0,
                    0.0,
                ],
            )

            project.add_structure(
                SceneStructure(
                    name=structure_data.get(
                        "name",
                        "",
                    ),

                    structure_type=structure_data.get(
                        "type",
                        "Unknown",
                    ),

                    position=(
                        position[0],
                        position[1],
                        position[2],
                    ),

                    rotation=(
                        rotation[0],
                        rotation[1],
                        rotation[2],
                    ),

                    length=structure_data.get(
                        "length",
                        0.0,
                    ),

                    properties=structure_data.get(
                        "properties",
                        {},
                    ),
                )
            )

        # Structure bindings

        for binding_data in data.get(
            "bindings",
            [],
        ):

            project.add_binding(
                StructureBinding(
                    structure_id=binding_data.get(
                        "structure_id",
                        "",
                    ),

                    fixtures=binding_data.get(
                        "fixtures",
                        [],
                    ),

                    properties=binding_data.get(
                        "properties",
                        {},
                    ),
                )
            )

        project.metadata = data.get(
            "metadata",
            {},
        )

        return project

    def load(
        self,
        path: str | Path,
    ) -> CaptureProject:
        """
        Load project from JSON file.
        """

        data = json.loads(
            Path(path).read_text(
                encoding="utf-8",
            )
        )

        return self.from_dict(
            data,
        )