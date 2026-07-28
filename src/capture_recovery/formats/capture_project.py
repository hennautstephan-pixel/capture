"""
Capture project output models.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .capture_group import (
    CaptureGroup,
)

from .capture_patch import (
    CapturePatch,
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

from .scene_structure import (
    SceneStructure,
)

from .structure_binding import (
    StructureBinding,
)

from .capture_scene import (
    CaptureScene,
)


@dataclass(slots=True)
class CaptureFixture:
    """
    Capture fixture model.
    """

    name: str

    universe: int = 0

    address: int = 0

    manufacturer: str | None = None

    model: str | None = None

    mode: str | None = None

    position: FixturePosition = field(
        default_factory=FixturePosition,
    )

    focus_point: FocusPoint = field(
        default_factory=FocusPoint,
    )

    mount: FixtureMount = field(
        default_factory=FixtureMount,
    )

    properties: dict = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class CaptureUniverse:
    """
    Capture universe model.
    """

    name: str

    universe: int = 0

    protocol: str | None = None

    properties: dict = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class CaptureCue:
    """
    Capture cue model.
    """

    name: str

    number: int = 0

    properties: dict = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class CaptureProject:
    """
    Complete Capture project model.
    """

    name: str

    fixtures: list[CaptureFixture] = field(
        default_factory=list,
    )

    universes: list[CaptureUniverse] = field(
        default_factory=list,
    )

    cues: list[CaptureCue] = field(
        default_factory=list,
    )

    patch: CapturePatch = field(
        default_factory=CapturePatch,
    )

    groups: list[CaptureGroup] = field(
        default_factory=list,
    )

    structures: list[SceneStructure] = field(
        default_factory=list,
    )

    bindings: list[StructureBinding] = field(
        default_factory=list,
    )

    scene: CaptureScene = field(
        default_factory=CaptureScene,
    )

    metadata: dict = field(
        default_factory=dict,
    )

    def add_fixture(
        self,
        fixture: CaptureFixture,
    ) -> None:

        self.fixtures.append(
            fixture,
        )

    def add_universe(
        self,
        universe: CaptureUniverse,
    ) -> None:

        self.universes.append(
            universe,
        )

    def add_cue(
        self,
        cue: CaptureCue,
    ) -> None:

        self.cues.append(
            cue,
        )

    def add_group(
        self,
        group: CaptureGroup,
    ) -> None:

        self.groups.append(
            group,
        )

    def add_structure(
        self,
        structure: SceneStructure,
    ) -> None:

        self.structures.append(
            structure,
        )

    def add_binding(
        self,
        binding: StructureBinding,
    ) -> None:

        self.bindings.append(
            binding,
        )

    def set_scene(
        self,
        scene: CaptureScene,
    ) -> None:
        """
        Attach scene graph.
        """

        self.scene = scene

    def __len__(
        self,
    ) -> int:
        """
        Return project object count.

        Kept for backward compatibility
        with existing serializers/tests.
        """

        return (
            len(self.fixtures)
            + len(self.universes)
            + len(self.cues)
            + len(self.groups)
            + len(self.structures)
            + len(self.bindings)
        )