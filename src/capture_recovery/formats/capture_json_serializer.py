"""
Capture JSON serializer.

Converts CaptureProject models into
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

from .fixture_mount import (
    FixtureMount,
)

from .structure_binding import (
    StructureBinding,
)

from .scene_structure import (
    SceneStructure,
)


class CaptureJsonSerializer:
    """
    Serialize Capture projects to JSON.
    """

    def to_dict(
        self,
        project: CaptureProject,
    ) -> dict:

        return {
            "project": {
                "name": project.name,
            },

            "fixtures": [
                self._fixture_to_dict(
                    fixture,
                )
                for fixture in project.fixtures
            ],

            "universes": [
                self._universe_to_dict(
                    universe,
                )
                for universe in project.universes
            ],

            "cues": [
                self._cue_to_dict(
                    cue,
                )
                for cue in project.cues
            ],

            "patch": self._patch_to_dict(
                project.patch,
            ),

            "groups": [
                self._group_to_dict(
                    group,
                )
                for group in project.groups
            ],

            "structures": [
                self._structure_to_dict(
                    structure,
                )
                for structure in project.structures
            ],

            "bindings": [
                self._binding_to_dict(
                    binding,
                )
                for binding in project.bindings
            ],

            "metadata": project.metadata.copy(),
        }

    def serialize(
        self,
        project: CaptureProject,
    ) -> dict:

        return self.to_dict(
            project,
        )

    def to_string(
        self,
        project: CaptureProject,
        indent: int = 2,
    ) -> str:

        return json.dumps(
            self.to_dict(
                project,
            ),
            indent=indent,
        )

    def save(
        self,
        project: CaptureProject,
        path: str | Path,
    ) -> None:

        Path(path).write_text(
            self.to_string(
                project,
            ),
            encoding="utf-8",
        )

    def _fixture_to_dict(
        self,
        fixture: CaptureFixture,
    ) -> dict:

        position = fixture.position

        focus = fixture.focus_point

        return {
            "name": fixture.name,

            "universe": fixture.universe,

            "address": fixture.address,

            "manufacturer": fixture.manufacturer,

            "model": fixture.model,

            "mode": fixture.mode,

            "position": {
                "x": position.x,
                "y": position.y,
                "z": position.z,
                "pan": position.pan,
                "tilt": position.tilt,
                "roll": position.roll,
            },

            "focus_point": {
                "x": focus.x,
                "y": focus.y,
                "z": focus.z,
            },

            "mount": self._mount_to_dict(
                fixture.mount,
            ),

            "properties": fixture.properties.copy(),
        }

    def _mount_to_dict(
        self,
        mount: FixtureMount,
    ) -> dict:

        return {
            "structure_id": mount.structure_id,

            "offset_x": mount.offset_x,

            "offset_y": mount.offset_y,

            "offset_z": mount.offset_z,

            "rotation": [
                mount.rotation[0],
                mount.rotation[1],
                mount.rotation[2],
            ],

            "properties": mount.properties.copy(),
        }

    def _binding_to_dict(
        self,
        binding: StructureBinding,
    ) -> dict:
        """
        Serialize structure binding.
        """

        return {
            "structure_id": binding.structure_id,

            "fixtures": [
                fixture
                for fixture in binding.fixtures
            ],

            "properties": binding.properties.copy(),
        }

    def _universe_to_dict(
        self,
        universe: CaptureUniverse,
    ) -> dict:

        return {
            "name": universe.name,

            "universe": universe.universe,

            "protocol": universe.protocol,

            "properties": universe.properties.copy(),
        }

    def _cue_to_dict(
        self,
        cue: CaptureCue,
    ) -> dict:

        return {
            "name": cue.name,

            "number": cue.number,

            "properties": cue.properties.copy(),
        }

    def _patch_to_dict(
        self,
        patch: CapturePatch,
    ) -> dict:

        return {
            "entries": [
                self._patch_entry_to_dict(
                    entry,
                )
                for entry in patch.entries
            ],
        }

    def _patch_entry_to_dict(
        self,
        entry: PatchEntry,
    ) -> dict:

        return {
            "fixture": entry.fixture,

            "universe": entry.universe,

            "address": entry.address,

            "mode": entry.mode,

            "channels": entry.channels,

            "properties": entry.properties.copy(),
        }

    def _group_to_dict(
        self,
        group: CaptureGroup,
    ) -> dict:

        return {
            "name": group.name,

            "fixtures": [
                fixture
                for fixture in group.fixtures
            ],

            "properties": group.properties.copy(),
        }

    def _structure_to_dict(
        self,
        structure: SceneStructure,
    ) -> dict:

        return {
            "name": structure.name,

            "type": structure.structure_type,

            "position": [
                structure.position[0],
                structure.position[1],
                structure.position[2],
            ],

            "rotation": [
                structure.rotation[0],
                structure.rotation[1],
                structure.rotation[2],
            ],

            "length": structure.length,

            "properties": structure.properties.copy(),
        }