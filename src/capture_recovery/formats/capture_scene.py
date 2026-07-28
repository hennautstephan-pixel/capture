"""
Capture scene model.

Contains the unified scene graph
for a Capture project.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .scene_node import (
    SceneNode,
)


@dataclass(slots=True)
class CaptureScene:
    """
    Unified Capture scene graph.
    """

    nodes: dict[str, SceneNode] = field(
        default_factory=dict,
    )

    root_nodes: list[str] = field(
        default_factory=list,
    )

    metadata: dict = field(
        default_factory=dict,
    )

    def add_node(
        self,
        node: SceneNode,
    ) -> None:
        """
        Add node to scene.
        """

        self.nodes[node.name] = node

        if node.parent is None:

            if node.name not in self.root_nodes:

                self.root_nodes.append(
                    node.name,
                )

    def get_node(
        self,
        name: str,
    ) -> SceneNode | None:
        """
        Find node by name.
        """

        return self.nodes.get(
            name,
        )

    def add_child_relation(
        self,
        parent: str,
        child: str,
    ) -> None:
        """
        Add parent-child relation.
        """

        parent_node = self.nodes.get(
            parent,
        )

        if parent_node is not None:

            parent_node.add_child(
                child,
            )