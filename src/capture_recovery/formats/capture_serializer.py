"""
Capture project serializer.

Converts recovered semantic objects into
Capture project models.
"""

from __future__ import annotations

from capture_recovery.models.project import Project

from .capture_fixture_builder import (
    CaptureFixtureBuilder,
)

from .capture_project import (
    CaptureCue,
    CaptureFixture,
    CaptureProject,
)

from .universe_builder import (
    UniverseBuilder,
)


class CaptureSerializer:
    """
    Serialize internal projects into Capture projects.
    """

    def __init__(
        self,
        fixture_builder: CaptureFixtureBuilder | None = None,
        universe_builder: UniverseBuilder | None = None,
    ) -> None:

        self.fixture_builder = fixture_builder

        self.universe_builder = (
            universe_builder
            or UniverseBuilder()
        )

    def serialize(
        self,
        project: Project,
    ) -> CaptureProject:
        """
        Convert a Project into a CaptureProject.
        """

        capture = CaptureProject(
            name=project.name,
        )

        self._serialize_fixtures(
            project,
            capture,
        )

        self._serialize_universes(
            project,
            capture,
        )

        self._serialize_cues(
            project,
            capture,
        )

        return capture

    def _serialize_fixtures(
        self,
        project: Project,
        capture: CaptureProject,
    ) -> None:
        """
        Serialize fixtures.

        Uses CaptureFixtureBuilder when available,
        otherwise creates a basic CaptureFixture.
        """

        for fixture in project.fixtures:

            if self.fixture_builder is not None:

                capture_fixture = (
                    self.fixture_builder.build(
                        fixture,
                    )
                )

            else:

                capture_fixture = CaptureFixture(
                    name=str(
                        fixture.identifier,
                    ),
                    universe=fixture.get(
                        "universe",
                        0,
                    ),
                    address=fixture.get(
                        "address",
                        0,
                    ),
                    manufacturer=fixture.get(
                        "manufacturer",
                    ),
                    model=fixture.get(
                        "model",
                    ),
                    mode=fixture.get(
                        "mode",
                    ),
                    properties=fixture.properties.copy(),
                )

            capture.add_fixture(
                capture_fixture,
            )

    def _serialize_universes(
        self,
        project: Project,
        capture: CaptureProject,
    ) -> None:
        """
        Serialize DMX universes.
        """

        for universe in project.universes:

            capture.add_universe(
                self.universe_builder.build(
                    universe,
                )
            )

    def _serialize_cues(
        self,
        project: Project,
        capture: CaptureProject,
    ) -> None:
        """
        Serialize cues.
        """

        for cue in project.cues:

            capture.add_cue(
                CaptureCue(
                    name=str(
                        cue.identifier,
                    ),
                    number=cue.get(
                        "cue_number",
                        0,
                    ),
                    properties=cue.properties.copy(),
                )
            )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(fixture_builder={self.fixture_builder!r}, "
            f"universe_builder={self.universe_builder!r})"
        )