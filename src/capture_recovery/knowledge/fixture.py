from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .semantic_object import SemanticObject


@dataclass(slots=True, frozen=True)
class Fixture(SemanticObject):
    """
    High-level representation of a Capture lighting fixture.

    A Fixture is produced by the KnowledgeEngine from one or more
    reconstructed binary structures.
    """

    name: str = ""

    manufacturer: str | None = None

    model: str | None = None

    mode: str | None = None

    universe: int | None = None

    address: int | None = None

    fixture_id: int | None = None

    position: tuple[float, float, float] | None = None

    rotation: tuple[float, float, float] | None = None

    scale: tuple[float, float, float] | None = None

    color: tuple[int, int, int] | None = None

    dimmer: float | None = None

    pan: float | None = None

    tilt: float | None = None

    zoom: float | None = None

    focus: float | None = None

    iris: float | None = None

    gobo: str | None = None

    frost: float | None = None

    enabled: bool = True

    locked: bool = False

    visible: bool = True

    def has_patch(self) -> bool:
        """
        Return True if the fixture has a valid DMX patch.
        """
        return (
            self.universe is not None
            and self.address is not None
        )

    def has_position(self) -> bool:
        """
        Return True if the fixture position is known.
        """
        return self.position is not None

    def has_rotation(self) -> bool:
        """
        Return True if the fixture orientation is known.
        """
        return self.rotation is not None

    def to_properties(self) -> dict[str, Any]:
        """
        Export fixture-specific properties as a dictionary.
        """

        return {
            "name": self.name,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "mode": self.mode,
            "universe": self.universe,
            "address": self.address,
            "fixture_id": self.fixture_id,
            "position": self.position,
            "rotation": self.rotation,
            "scale": self.scale,
            "color": self.color,
            "dimmer": self.dimmer,
            "pan": self.pan,
            "tilt": self.tilt,
            "zoom": self.zoom,
            "focus": self.focus,
            "iris": self.iris,
            "gobo": self.gobo,
            "frost": self.frost,
            "enabled": self.enabled,
            "locked": self.locked,
            "visible": self.visible,
        }