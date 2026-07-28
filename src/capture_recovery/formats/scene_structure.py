"""
Scene structure models.

Contains rigging elements used by
Capture projects.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SceneStructure:
    """
    Generic scene rigging element.
    """

    name: str

    structure_type: str = "Unknown"

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

    length: float = 0.0

    properties: dict = field(
        default_factory=dict,
    )