"""
Fixture definition model.

Describes a lighting fixture from a library.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class FixtureDefinition:
    """
    Lighting fixture definition.
    """

    manufacturer: str

    model: str

    modes: list[str] = field(
        default_factory=list,
    )

    channels: dict[str, int] = field(
        default_factory=dict,
    )

    geometry: dict[str, Any] = field(
        default_factory=dict,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def name(self) -> str:
        return (
            f"{self.manufacturer} "
            f"{self.model}"
        )

    def has_mode(
        self,
        mode: str,
    ) -> bool:
        return mode in self.modes

    def channel(
        self,
        name: str,
    ) -> int | None:

        return self.channels.get(
            name,
        )