"""
Scene hierarchy resolver.

Computes world transformations through
parent/child relationships.
"""

from __future__ import annotations

from .scene_node import (
    SceneNode,
)

from .spatial_transform import (
    SpatialTransform,
)

from .world_position import (
    WorldPosition,
)


class HierarchyResolver:
    """
    Resolve hierarchical transforms.
    """

    def __init__(
        self,
        transform=None,
    ):

        self.transform = (
            transform
            or SpatialTransform()
        )

    def resolve(
        self,
        node_name: str,
        nodes: dict[str, SceneNode],
    ) -> WorldPosition:

        node = nodes[node_name]

        if node.parent is None:

            return WorldPosition(
                x=node.position[0],
                y=node.position[1],
                z=node.position[2],
            )

        parent_world = self.resolve(
            node.parent,
            nodes,
        )

        local = (
            node.position[0],
            node.position[1],
            node.position[2],
        )

        return self.transform.transform_position(
            local,

            (
                parent_world.x,
                parent_world.y,
                parent_world.z,
            ),

            node.rotation,
        )