"""
Fast index for MemoryMap.

Provides efficient lookup by offset.
"""

from __future__ import annotations

from bisect import bisect_right

from .memory_map import MemoryMap
from .region import MemoryRegion


class MemoryIndex:
    """
    Fast lookup structure for MemoryRegion objects.
    """

    def __init__(self, memory: MemoryMap):

        self._regions = memory.regions

        self._offsets = [
            region.offset
            for region in self._regions
        ]

    def __len__(self) -> int:
        return len(self._regions)

    def at(
        self,
        offset: int,
    ) -> MemoryRegion | None:
        """
        Return the region containing an offset.
        """

        position = bisect_right(
            self._offsets,
            offset,
        ) - 1

        if position < 0:
            return None

        region = self._regions[position]

        if offset in region:
            return region

        return None

    def before(
        self,
        offset: int,
    ) -> MemoryRegion | None:
        """
        Return previous region.
        """

        position = bisect_right(
            self._offsets,
            offset,
        ) - 1

        if position < 0:
            return None

        return self._regions[position]

    def after(
        self,
        offset: int,
    ) -> MemoryRegion | None:
        """
        Return first region after offset.
        """

        position = bisect_right(
            self._offsets,
            offset,
        )

        if position >= len(self._regions):
            return None

        return self._regions[position]

    def between(
        self,
        start: int,
        end: int,
    ) -> list[MemoryRegion]:
        """
        Return regions intersecting a range.
        """

        result = []

        for region in self._regions:

            if region.end <= start:
                continue

            if region.offset >= end:
                break

            result.append(region)

        return result

    def by_kind(
        self,
        kind: str,
    ) -> list[MemoryRegion]:

        return [
            region
            for region in self._regions
            if region.kind == kind
        ]