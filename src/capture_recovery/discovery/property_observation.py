"""
Property observation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class PropertyObservation:
    """
    Observation collected while comparing two Capture projects.

    An observation links a binary modification with its corresponding
    semantic modification.
    """

    object_type: str

    offset: int

    semantic_property: str

    binary_before: Any

    binary_after: Any

    semantic_before: Any

    semantic_after: Any

    @property
    def identifier(self) -> str:
        """
        Stable identifier of the observed property.
        """
        return (
            f"{self.object_type}:"
            f"{self.semantic_property}:"
            f"0x{self.offset:X}"
        )

    @property
    def binary_changed(self) -> bool:
        """
        True if the binary value changed.
        """
        return self.binary_before != self.binary_after

    @property
    def semantic_changed(self) -> bool:
        """
        True if the semantic value changed.
        """
        return self.semantic_before != self.semantic_after

    @property
    def is_consistent(self) -> bool:
        """
        True when binary and semantic changes are consistent.
        """
        return (
            self.binary_changed
            == self.semantic_changed
        )