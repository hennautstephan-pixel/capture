"""
Scene structure builder.

Builds rigging objects from
semantic objects.
"""

from __future__ import annotations

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from .scene_structure import (
    SceneStructure,
)


class StructureBuilder:
    """
    Build scene structures.
    """

    def build(
        self,
        obj: SemanticObject,
    ) -> SceneStructure:
        """
        Convert semantic structure.
        """

        position = obj.properties.get(
            "position",
            (
                0.0,
                0.0,
                0.0,
            ),
        )

        rotation = obj.properties.get(
            "rotation",
            (
                0.0,
                0.0,
                0.0,
            ),
        )

        return SceneStructure(
            name=str(
                obj.identifier,
            ),

            structure_type=obj.properties.get(
                "type",
                "Unknown",
            ),

            position=position,

            rotation=rotation,

            length=obj.properties.get(
                "length",
                0.0,
            ),

            properties=obj.properties.copy(),
        )

    def can_build(
        self,
        obj: SemanticObject,
    ) -> bool:
        """
        Check structure type.
        """

        return obj.object_type == "Structure"