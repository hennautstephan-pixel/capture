"""
Scene reconstruction.

Builds a CaptureScene using semantic objects
and their relations.
"""

from __future__ import annotations

from capture_recovery.formats import (
    CaptureScene,
    SceneNode,
)


from capture_recovery.analysis import (
    RelationGraph,
)


from .relation_applier import (
    RelationApplier,
)


class SceneReconstruction:
    """
    Reconstruct complete scene hierarchy.
    """

    def __init__(
        self,
        relation_applier=None,
    ) -> None:

        self.relation_applier = (
            relation_applier
            or RelationApplier()
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

            node = SceneNode(
                name=str(
                    obj.identifier,
                ),

                properties=(
                    obj.properties.copy()
                ),
            )

            scene.add_node(
                node,
            )


        self.relation_applier.apply(
            scene,
            graph,
        )


        return scene