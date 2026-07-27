"""
Universe builder.

Builds CaptureUniverse objects from recovered
semantic universes.
"""

from __future__ import annotations

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from .capture_project import (
    CaptureUniverse,
)


class UniverseBuilder:
    """
    Build Capture DMX universes.
    """

    def build(
        self,
        universe: SemanticObject,
    ) -> CaptureUniverse:
        """
        Convert a semantic universe into
        a CaptureUniverse.
        """

        return CaptureUniverse(
            name=str(
                universe.identifier,
            ),
            universe=universe.get(
                "universe",
                0,
            ),
            protocol=universe.get(
                "protocol",
            ),
            properties={
                **universe.properties,
            },
        )

    def can_build(
        self,
        universe: SemanticObject,
    ) -> bool:
        """
        Return True if the object is a universe.
        """

        return (
            universe.object_type
            == "Universe"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}()"
        )