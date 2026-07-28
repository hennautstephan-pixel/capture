"""
Relation applier.

Applies semantic relations to reconstructed scenes.
"""

from __future__ import annotations

from capture_recovery.analysis import (
    RelationGraph,
)

from capture_recovery.formats import (
    CaptureScene,
)


class RelationApplier:
    """
    Apply relation graph to a CaptureScene.
    """

    def apply(
        self,
        scene: CaptureScene,
        graph: RelationGraph,
    ) -> CaptureScene:
        """
        Apply all relations to scene nodes.
        """

        for relation in graph.relations:

            source = scene.get_node(
                relation.source,
            )

            target = scene.get_node(
                relation.target,
            )

            if source is None or target is None:
                continue


            if relation.relation_type in (
                "child_of",
                "mounted_on",
            ):

                source.parent = (
                    target.name
                )

                target.add_child(
                    source.name,
                )


        return scene