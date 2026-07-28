"""
Scene hierarchy node.

Represents an object in the scene graph.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SceneNode:
    """
    Node in a hierarchical scene graph.
    """

    name: str

    parent: str | None = None

    position: tuple[float, float, float] = (
        0.0,
        0.0,
        0.0,
    )

    rotation: tuple[float, float, float] = (
        0.0,
        0.0,
        0.0,
    )

    children: list[str] = field(
        default_factory=list,
    )

    properties: dict = field(
        default_factory=dict,
    )

    def add_child(
        self,
        child: str,
    ) -> None:
        """
        Add child reference.
        """

        if child not in self.children:

            self.children.append(
                child,
            )