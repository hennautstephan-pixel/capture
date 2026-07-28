"""
Scene transform node builder.
"""

from __future__ import annotations

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from .scene_node import (
    SceneNode,
)


class TransformNodeBuilder:
    """
    Build scene nodes from semantic objects.
    """

    def can_build(
        self,
        obj: SemanticObject,
    ) -> bool:

        return obj.object_type in (
            "Scene",
            "Structure",
            "Fixture",
            "Object",
        )

    def build(
        self,
        obj: SemanticObject,
    ) -> SceneNode:

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

        return SceneNode(
            name=str(
                obj.identifier,
            ),

            parent=obj.properties.get(
                "parent",
            ),

            position=(
                position[0],
                position[1],
                position[2],
            ),

            rotation=(
                rotation[0],
                rotation[1],
                rotation[2],
            ),

            properties=obj.properties.copy(),
        )