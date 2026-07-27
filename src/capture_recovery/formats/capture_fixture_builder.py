"""
Capture fixture builder.

Builds CaptureFixture objects from recovered
semantic fixtures using fixture library and geometry.
"""

from __future__ import annotations

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from capture_recovery.library.fixture_resolver import (
    FixtureResolver,
)

from .capture_project import (
    CaptureFixture,
)

from .fixture_geometry_builder import (
    FixtureGeometryBuilder,
)


class CaptureFixtureBuilder:
    """
    Build enriched Capture fixtures.
    """

    def __init__(
        self,
        resolver: FixtureResolver,
        geometry_builder: FixtureGeometryBuilder | None = None,
    ) -> None:

        self.resolver = resolver

        self.geometry_builder = (
            geometry_builder
            or FixtureGeometryBuilder()
        )

    def build(
        self,
        fixture: SemanticObject,
    ) -> CaptureFixture:
        """
        Convert a semantic fixture into
        a CaptureFixture.
        """

        definition = self.resolver.resolve(
            fixture,
        )

        properties = fixture.properties.copy()

        # Fixture library enrichment
        if definition is not None:

            properties.update(
                {
                    "channels": definition.channels,
                    "modes": definition.modes,
                    "library": definition.name,
                }
            )

            # Optical / physical fixture data
            # (beam angle, zoom, dimensions...)
            if definition.geometry:

                properties[
                    "geometry"
                ] = definition.geometry

        # Scene placement geometry
        placement = self.geometry_builder.build(
            fixture,
        )

        properties[
            "placement"
        ] = placement.to_dict()

        return CaptureFixture(
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
            properties=properties,
        )

    def can_build(
        self,
        fixture: SemanticObject,
    ) -> bool:
        """
        Return True if the object is a fixture.
        """

        return fixture.object_type == "Fixture"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(resolver={self.resolver!r})"
        )