"""
Binary object relationship graph.

This module stores relationships between BinaryObject instances without
performing any semantic interpretation.

The graph is directed:

    source ----> target

Typical usages:

- Which objects reference object X?
- Which objects are referenced by object X?
- Detect isolated objects.
- Detect cycles.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator

from .binary_reference import BinaryReference


class BinaryGraph:
    """
    Directed graph of BinaryObject relationships.

    The graph stores only identifiers. BinaryObject instances remain
    inside BinaryIndex.
    """

    def __init__(self) -> None:
        self._children: dict[int, set[int]] = defaultdict(set)
        self._parents: dict[int, set[int]] = defaultdict(set)
        self._references: list[BinaryReference] = []

    def __len__(self) -> int:
        return len(self._references)

    def __iter__(self) -> Iterator[BinaryReference]:
        return iter(self._references)

    def add(self, reference: BinaryReference) -> None:
        """
        Add a new directed relationship.
        """

        self._references.append(reference)

        self._children[reference.source].add(reference.target)
        self._parents[reference.target].add(reference.source)

    def children(self, identifier: int) -> frozenset[int]:
        """
        Objects referenced by identifier.
        """

        return frozenset(self._children.get(identifier, ()))

    def parents(self, identifier: int) -> frozenset[int]:
        """
        Objects referencing identifier.
        """

        return frozenset(self._parents.get(identifier, ()))

    def has_children(self, identifier: int) -> bool:
        return identifier in self._children

    def has_parents(self, identifier: int) -> bool:
        return identifier in self._parents

    def is_isolated(self, identifier: int) -> bool:
        """
        Object has no incoming and no outgoing references.
        """

        return (
            identifier not in self._children
            and identifier not in self._parents
        )

    def clear(self) -> None:
        """
        Remove every relationship.
        """

        self._references.clear()
        self._children.clear()
        self._parents.clear()

    @property
    def references(self) -> tuple[BinaryReference, ...]:
        """
        Immutable view of every reference.
        """

        return tuple(self._references)