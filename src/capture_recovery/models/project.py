"""
Capture project semantic model.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


@dataclass(slots=True)
class Project:
    """
    Reconstructed Capture project.

    Contains semantic objects grouped by type.
    """

    name: str = "Recovered Project"

    objects: list[SemanticObject] = field(
        default_factory=list,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    @property
    def fixtures(self) -> tuple[SemanticObject, ...]:
        """Return all fixtures."""
        return tuple(
            obj
            for obj in self.objects
            if obj.object_type == "Fixture"
        )

    @property
    def universes(self) -> tuple[SemanticObject, ...]:
        """Return all universes."""
        return tuple(
            obj
            for obj in self.objects
            if obj.object_type == "Universe"
        )

    @property
    def cues(self) -> tuple[SemanticObject, ...]:
        """Return all cues."""
        return tuple(
            obj
            for obj in self.objects
            if obj.object_type == "Cue"
        )

    @property
    def object_types(self) -> tuple[str, ...]:
        """Return all known object types."""
        return tuple(
            sorted(
                {
                    obj.object_type
                    for obj in self.objects
                }
            )
        )

    def add(
        self,
        obj: SemanticObject,
    ) -> None:
        """Add a semantic object."""
        self.objects.append(obj)

    def extend(
        self,
        objects: Iterable[SemanticObject],
    ) -> None:
        """Add multiple semantic objects."""
        self.objects.extend(objects)

    def remove(
        self,
        obj: SemanticObject,
    ) -> None:
        """Remove a semantic object."""
        self.objects.remove(obj)

    def clear(self) -> None:
        """Remove every object."""
        self.objects.clear()

    def find(
        self,
        object_type: str,
        identifier: str | int,
    ) -> SemanticObject | None:
        """Find an object by type and identifier."""
        for obj in self.objects:
            if (
                obj.object_type == object_type
                and obj.identifier == identifier
            ):
                return obj

        return None

    def count(
        self,
        object_type: str | None = None,
    ) -> int:
        """Count objects."""
        if object_type is None:
            return len(self.objects)

        return sum(
            1
            for obj in self.objects
            if obj.object_type == object_type
        )

    def statistics(self) -> dict[str, int]:
        """
        Return the number of objects grouped by type.
        """
        return dict(
            Counter(
                obj.object_type
                for obj in self.objects
            )
        )

    def __len__(self) -> int:
        return len(self.objects)

    def __iter__(self):
        return iter(self.objects)

    def __repr__(self) -> str:
        return (
            f"Project("
            f"name={self.name!r}, "
            f"objects={len(self.objects)})"
        )