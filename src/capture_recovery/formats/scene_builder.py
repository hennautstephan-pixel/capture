"""
Capture scene builder.

Builds a scene graph from semantic objects.
"""

from __future__ import annotations

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from .capture_scene import (
    CaptureScene,
)

from .transform_node_builder import (
    TransformNodeBuilder,
)


class SceneBuilder:
    """
    Build CaptureScene objects.
    """

    def __init__(
        self,
        node_builder=None,
    ) -> None:

        self.node_builder = (
            node_builder
            or TransformNodeBuilder()
        )

    def build(
        self,
        objects,
    ) -> CaptureScene:
        """
        Build complete scene graph.
        """

        scene = CaptureScene()

        for obj in objects:

            if self.node_builder.can_build(
                obj,
            ):

                node = (
                    self.node_builder.build(
                        obj,
                    )
                )

                scene.add_node(
                    node,
                )

        self._resolve_children(
            scene,
        )

        return scene

    def _resolve_children(
        self,
        scene: CaptureScene,
    ) -> None:
        """
        Build child references.
        """

        for node in scene.nodes.values():

            if node.parent is None:
                continue

            scene.add_child_relation(
                node.parent,
                node.name,
            )