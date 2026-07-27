"""
Fixture library registry.
"""

from __future__ import annotations

from .fixture_definition import FixtureDefinition


class FixtureLibrary:
    """
    Registry of known lighting fixtures.
    """

    def __init__(self) -> None:

        self._fixtures: dict[
            tuple[str, str],
            FixtureDefinition,
        ] = {}

    def register(
        self,
        fixture: FixtureDefinition,
    ) -> None:

        key = (
            fixture.manufacturer.lower(),
            fixture.model.lower(),
        )

        self._fixtures[key] = fixture

    def find(
        self,
        manufacturer: str,
        model: str,
    ) -> FixtureDefinition | None:

        key = (
            manufacturer.lower(),
            model.lower(),
        )

        return self._fixtures.get(
            key,
        )

    def __len__(self) -> int:
        return len(
            self._fixtures,
        )

    def __iter__(self):

        return iter(
            self._fixtures.values(),
        )