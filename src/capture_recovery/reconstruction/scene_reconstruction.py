"""
Scene reconstruction.

Builds a CaptureScene using semantic objects
and their relations.
"""

from __future__ import annotations

from capture_recovery.analysis import RelationGraph
from capture_recovery.formats import CaptureScene, SceneNode

from .relation_applier import RelationApplier


class SceneReconstruction:
    """
    Reconstruct complete scene hierarchy.
    """

    def __init__(self, relation_applier=None) -> None:
        self.relation_applier = relation_applier or RelationApplier()

    @staticmethod
    def _build_node(obj) -> SceneNode:
        return SceneNode(
            name=str(obj.identifier),
            properties=obj.properties.copy(),
        )

    def build(
        self,
        objects,
        graph: RelationGraph,
    ) -> CaptureScene:
        """
        Build scene graph.
        """
        scene = CaptureScene()

        for obj in objects:
            scene.add_node(self._build_node(obj))

        self.relation_applier.apply(scene, graph)
        return scene