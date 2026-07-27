"""
Fixture resolver.

Links recovered semantic fixtures with
known fixture definitions from the library.
"""

from __future__ import annotations

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from .fixture_definition import FixtureDefinition
from .fixture_library import FixtureLibrary


class FixtureResolver:
    """
    Resolve semantic fixtures using a fixture library.
    """

    def __init__(
        self,
        library: FixtureLibrary,
    ) -> None:

        self.library = library

    def resolve(
        self,
        fixture: SemanticObject,
    ) -> FixtureDefinition | None:
        """
        Find the matching fixture definition.
        """

        if fixture.object_type != "Fixture":
            return None

        manufacturer = fixture.get(
            "manufacturer",
        )

        model = fixture.get(
            "model",
        )

        if not manufacturer or not model:
            return None

        return self.library.find(
            manufacturer,
            model,
        )

    def can_resolve(
        self,
        fixture: SemanticObject,
    ) -> bool:
        """
        Return True if a fixture definition exists.
        """

        return (
            self.resolve(
                fixture,
            )
            is not None
        )

    def enrich(
        self,
        fixture: SemanticObject,
    ) -> dict:
        """
        Return fixture data enriched with library data.
        """

        definition = self.resolve(
            fixture,
        )

        if definition is None:
            return fixture.properties.copy()

        data = fixture.properties.copy()

        data.update(
            {
                "library_manufacturer": definition.manufacturer,
                "library_model": definition.model,
                "library_modes": definition.modes,
                "library_channels": definition.channels,
                "library_geometry": definition.geometry,
            }
        )

        return data

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(fixtures={len(self.library)})"
        )