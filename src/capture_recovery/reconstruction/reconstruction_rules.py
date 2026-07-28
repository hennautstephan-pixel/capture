"""
Reconstruction rules.

Defines how semantic objects are
converted into Capture project data.
"""

from __future__ import annotations


class ReconstructionRules:
    """
    Default reconstruction rules.
    """

    FIXTURE_TYPES = (
        "Fixture",
        "Projector",
        "Light",
    )

    STRUCTURE_TYPES = (
        "Structure",
        "Truss",
        "Rig",
    )

    GROUP_TYPES = (
        "Group",
    )

    def is_fixture(
        self,
        obj,
    ) -> bool:
        return obj.object_type in (
            self.FIXTURE_TYPES
        )

    def is_structure(
        self,
        obj,
    ) -> bool:
        return obj.object_type in (
            self.STRUCTURE_TYPES
        )

    def is_group(
        self,
        obj,
    ) -> bool:
        return obj.object_type in (
            self.GROUP_TYPES
        )