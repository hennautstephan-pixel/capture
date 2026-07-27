"""
Capture project format model.

Represents a project ready for serialization
to a Capture compatible format.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CaptureFixture:
    """
    Capture fixture representation.
    """

    name: str

    universe: int

    address: int

    manufacturer: str | None = None

    model: str | None = None

    mode: str | None = None

    properties: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class CaptureUniverse:
    """
    Capture DMX universe representation.
    """

    name: str

    universe: int

    protocol: str | None = None

    properties: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class CaptureCue:
    """
    Capture cue representation.
    """

    name: str

    number: int

    properties: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class CaptureProject:
    """
    Serializable Capture project model.
    """

    name: str = "Recovered Capture Project"

    fixtures: list[CaptureFixture] = field(
        default_factory=list,
    )

    universes: list[CaptureUniverse] = field(
        default_factory=list,
    )

    cues: list[CaptureCue] = field(
        default_factory=list,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    def add_fixture(
        self,
        fixture: CaptureFixture,
    ) -> None:
        self.fixtures.append(
            fixture,
        )

    def add_universe(
        self,
        universe: CaptureUniverse,
    ) -> None:
        self.universes.append(
            universe,
        )

    def add_cue(
        self,
        cue: CaptureCue,
    ) -> None:
        self.cues.append(
            cue,
        )

    def count(self) -> int:
        return (
            len(self.fixtures)
            + len(self.universes)
            + len(self.cues)
        )

    def __len__(self) -> int:
        return self.count()