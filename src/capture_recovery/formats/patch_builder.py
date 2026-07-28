"""
DMX patch builder.

Builds CapturePatch objects from recovered
semantic fixture objects.
"""

from __future__ import annotations

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from .capture_patch import (
    CapturePatch,
    PatchEntry,
)


class PatchBuilder:
    """
    Build DMX patch information.
    """

    def build(
        self,
        fixtures: list[SemanticObject]
        | tuple[SemanticObject, ...],
    ) -> CapturePatch:
        """
        Convert fixtures into a DMX patch.
        """

        patch = CapturePatch()

        for fixture in fixtures:

            patch.add(
                self._build_entry(
                    fixture,
                )
            )

        return patch

    def _build_entry(
        self,
        fixture: SemanticObject,
    ) -> PatchEntry:
        """
        Build one patch entry.
        """

        return PatchEntry(
            fixture=str(
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
            mode=fixture.get(
                "mode",
            ),
            channels=fixture.get(
                "channels",
                0,
            ),
            properties={
                **fixture.properties,
            },
        )

    def can_build(
        self,
        fixture: SemanticObject,
    ) -> bool:
        """
        Return True if the object can be patched.
        """

        return (
            fixture.object_type
            == "Fixture"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}()"
        )