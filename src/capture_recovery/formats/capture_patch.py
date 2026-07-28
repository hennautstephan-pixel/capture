"""
Capture DMX patch models.

Contains patch entries linking fixtures
to DMX universes and addresses.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PatchEntry:
    """
    DMX patch entry.

    Represents one fixture assignment
    in a DMX universe.
    """

    fixture: str

    universe: int = 0

    address: int = 0

    mode: str | None = None

    channels: int = 0

    properties: dict = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class CapturePatch:
    """
    Complete DMX patch.

    Contains all fixture assignments.
    """

    entries: list[PatchEntry] = field(
        default_factory=list,
    )

    def add(
        self,
        entry: PatchEntry,
    ) -> None:
        """
        Add a patch entry.
        """

        self.entries.append(
            entry,
        )

    def __len__(self) -> int:
        return len(
            self.entries,
        )

    def __iter__(self):
        return iter(
            self.entries,
        )