"""
Cue builder.

Builds CaptureCue objects from recovered
semantic cue objects.
"""

from __future__ import annotations

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from .capture_project import (
    CaptureCue,
)


class CueBuilder:
    """
    Build Capture cues.
    """

    def build(
        self,
        cue: SemanticObject,
    ) -> CaptureCue:
        """
        Convert a semantic cue into
        a CaptureCue.
        """

        return CaptureCue(
            name=str(
                cue.identifier,
            ),
            number=cue.get(
                "cue_number",
                0,
            ),
            properties={
                **cue.properties,
            },
        )

    def can_build(
        self,
        cue: SemanticObject,
    ) -> bool:
        """
        Return True if the object is a cue.
        """

        return (
            cue.object_type
            == "Cue"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}()"
        )