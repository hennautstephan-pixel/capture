from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class SemanticObject:
    """
    High-level semantic object inferred from reconstructed structures.

    Instances are immutable and hashable, making them suitable for use
    in indexes, sets and caches.
    """

    object_type: str

    identifier: str | int

    properties: dict[str, object] = field(default_factory=dict)

    confidence: float = 1.0

    def get(
        self,
        name: str,
        default: object = None,
    ) -> object:
        """
        Return a property value.

        Equivalent to dict.get().
        """
        return self.properties.get(name, default)

    def has(
        self,
        name: str,
    ) -> bool:
        """
        Return True if a property exists.
        """
        return name in self.properties

    @property
    def key(self) -> tuple[str, str | int]:
        """
        Unique object key.
        """
        return (
            self.object_type,
            self.identifier,
        )

    @property
    def property_names(self) -> tuple[str, ...]:
        """
        Return all property names sorted alphabetically.
        """
        return tuple(sorted(self.properties))

    @property
    def property_count(self) -> int:
        """
        Return the number of properties.
        """
        return len(self.properties)

    def with_confidence(
        self,
        confidence: float,
    ) -> "SemanticObject":
        """
        Return a copy with a different confidence.
        """
        return SemanticObject(
            object_type=self.object_type,
            identifier=self.identifier,
            properties=dict(self.properties),
            confidence=confidence,
        )

    def with_property(
        self,
        name: str,
        value: Any,
    ) -> "SemanticObject":
        """
        Return a copy with one modified property.
        """
        props = dict(self.properties)
        props[name] = value

        return SemanticObject(
            object_type=self.object_type,
            identifier=self.identifier,
            properties=props,
            confidence=self.confidence,
        )

    def __contains__(
        self,
        name: str,
    ) -> bool:
        return name in self.properties

    def __len__(self) -> int:
        return len(self.properties)

    def __repr__(self) -> str:
        return (
            f"SemanticObject("
            f"type={self.object_type!r}, "
            f"id={self.identifier!r}, "
            f"properties={len(self.properties)}, "
            f"confidence={self.confidence:.2f})"
        )