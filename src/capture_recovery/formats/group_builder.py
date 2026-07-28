"""
Fixture group builder.

Builds Capture groups from recovered
semantic objects.
"""

from __future__ import annotations

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from .capture_group import (
    CaptureGroup,
)


class GroupBuilder:
    """
    Build fixture groups.
    """

    def build(
        self,
        group: SemanticObject,
    ) -> CaptureGroup:
        """
        Convert semantic group object.
        """

        result = CaptureGroup(
            name=str(
                group.identifier,
            ),
        )

        fixtures = group.get(
            "fixtures",
            [],
        )

        for fixture in fixtures:

            result.add_fixture(
                str(fixture),
            )

        result.properties = (
            group.properties.copy()
        )

        return result

    def can_build(
        self,
        obj: SemanticObject,
    ) -> bool:
        """
        Check semantic type.
        """

        return (
            obj.object_type
            == "Group"
        )