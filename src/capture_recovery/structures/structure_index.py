from __future__ import annotations

from bisect import bisect_left, bisect_right

from .structure import Structure


class StructureIndex:
    """
    Fast lookup index for reconstructed structures.
    """

    def __init__(
        self,
        structures: list[Structure],
    ) -> None:

        self._structures = sorted(
            structures,
            key=lambda s: s.offset,
        )

        self._offsets = [
            s.offset
            for s in self._structures
        ]

    # -------------------------------------------------------------

    def all(self) -> list[Structure]:
        return self._structures

    # -------------------------------------------------------------

    def at(
        self,
        offset: int,
    ) -> list[Structure]:
        """
        Structures beginning exactly at offset.
        """

        left = bisect_left(self._offsets, offset)
        right = bisect_right(self._offsets, offset)

        return self._structures[left:right]

    # -------------------------------------------------------------

    def before(
        self,
        offset: int,
    ) -> list[Structure]:

        index = bisect_left(
            self._offsets,
            offset,
        )

        return self._structures[:index]

    # -------------------------------------------------------------

    def after(
        self,
        offset: int,
    ) -> list[Structure]:

        index = bisect_right(
            self._offsets,
            offset,
        )

        return self._structures[index:]

    # -------------------------------------------------------------

    def between(
        self,
        start: int,
        end: int,
    ) -> list[Structure]:

        left = bisect_left(
            self._offsets,
            start,
        )

        right = bisect_left(
            self._offsets,
            end,
        )

        return self._structures[left:right]

    # -------------------------------------------------------------

    def overlapping(
        self,
        start: int,
        end: int,
    ) -> list[Structure]:

        return [
            s
            for s in self._structures
            if s.offset < end
            and s.end > start
        ]

    # -------------------------------------------------------------

    def by_name(
        self,
        name: str,
    ) -> list[Structure]:

        return [
            s
            for s in self._structures
            if s.name == name
        ]

    # -------------------------------------------------------------

    def first(self) -> Structure | None:

        if not self._structures:
            return None

        return self._structures[0]

    # -------------------------------------------------------------

    def last(self) -> Structure | None:

        if not self._structures:
            return None

        return self._structures[-1]

    # -------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._structures)

    def __iter__(self):
        return iter(self._structures)