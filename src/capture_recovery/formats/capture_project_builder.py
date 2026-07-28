"""
Capture project builder.

Builds complete Capture projects
from semantic objects.
"""

from __future__ import annotations

from .capture_project import (
    CaptureProject,
)

from .cue_builder import (
    CueBuilder,
)

from .group_builder import (
    GroupBuilder,
)

from .patch_builder import (
    PatchBuilder,
)

from .structure_builder import (
    StructureBuilder,
)

from .universe_builder import (
    UniverseBuilder,
)

from .binding_builder import (
    BindingBuilder,
)

from .scene_builder import (
    SceneBuilder,
)


class CaptureProjectBuilder:
    """
    Build complete Capture projects.
    """

    def __init__(
        self,
        fixture_builder=None,
        universe_builder=None,
        cue_builder=None,
        patch_builder=None,
        group_builder=None,
        structure_builder=None,
        binding_builder=None,
        scene_builder=None,
    ) -> None:

        self.fixture_builder = (
            fixture_builder
        )

        self.universe_builder = (
            universe_builder
            or UniverseBuilder()
        )

        self.cue_builder = (
            cue_builder
            or CueBuilder()
        )

        self.patch_builder = (
            patch_builder
            or PatchBuilder()
        )

        self.group_builder = (
            group_builder
            or GroupBuilder()
        )

        self.structure_builder = (
            structure_builder
            or StructureBuilder()
        )

        self.binding_builder = (
            binding_builder
            or BindingBuilder()
        )

        self.scene_builder = (
            scene_builder
            or SceneBuilder()
        )

    def build(
        self,
        objects,
        name: str | None = None,
    ) -> CaptureProject:

        project = CaptureProject(
            name=(
                name
                or self._extract_project_name(
                    objects,
                )
                or "Recovered Capture"
            ),
        )

        self._build_fixtures(
            project,
            objects,
        )

        self._build_universes(
            project,
            objects,
        )

        self._build_cues(
            project,
            objects,
        )

        self._build_groups(
            project,
            objects,
        )

        self._build_structures(
            project,
            objects,
        )

        self._build_patch(
            project,
            objects,
        )

        self._build_bindings(
            project,
        )

        self._build_scene(
            project,
            objects,
        )

        return project

    def _extract_project_name(
        self,
        objects,
    ):

        if hasattr(
            objects,
            "name",
        ):
            return objects.name

        for obj in objects:

            if obj.object_type == "Project":

                return str(
                    obj.identifier,
                )

        return None

    def _build_fixtures(
        self,
        project,
        objects,
    ):

        if self.fixture_builder is None:
            return

        for obj in objects:

            if self.fixture_builder.can_build(
                obj,
            ):

                project.add_fixture(
                    self.fixture_builder.build(
                        obj,
                    )
                )

    def _build_universes(
        self,
        project,
        objects,
    ):

        for obj in objects:

            if self.universe_builder.can_build(
                obj,
            ):

                project.add_universe(
                    self.universe_builder.build(
                        obj,
                    )
                )

    def _build_cues(
        self,
        project,
        objects,
    ):

        for obj in objects:

            if self.cue_builder.can_build(
                obj,
            ):

                project.add_cue(
                    self.cue_builder.build(
                        obj,
                    )
                )

    def _build_groups(
        self,
        project,
        objects,
    ):

        for obj in objects:

            if self.group_builder.can_build(
                obj,
            ):

                project.add_group(
                    self.group_builder.build(
                        obj,
                    )
                )

    def _build_structures(
        self,
        project,
        objects,
    ):

        for obj in objects:

            if self.structure_builder.can_build(
                obj,
            ):

                project.add_structure(
                    self.structure_builder.build(
                        obj,
                    )
                )

    def _build_bindings(
        self,
        project,
    ):

        bindings = self.binding_builder.build(
            project,
        )

        for binding in bindings:

            project.add_binding(
                binding,
            )

    def _build_scene(
        self,
        project,
        objects,
    ):

        project.set_scene(
            self.scene_builder.build(
                objects,
            )
        )

    def _build_patch(
        self,
        project,
        objects,
    ):

        project.patch = (
            self.patch_builder.build(
                objects,
            )
        )