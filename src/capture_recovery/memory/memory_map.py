"""
Memory map.

A MemoryMap contains every logical region identified in a Capture file.

It provides fast iteration, validation and helper methods used by
high-level analyzers.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator

from .region import MemoryRegion


class MemoryMap:
    """
    Collection of MemoryRegion objects.

    Regions are always returned sorted by offset.
    """

    def __init__(self) -> None:
        self._regions: list[MemoryRegion] = []

    # ------------------------------------------------------------------
    # Collection API
    # ------------------------------------------------------------------

    def __iter__(self) -> Iterator[MemoryRegion]:
        return iter(self.regions)

    def __len__(self) -> int:
        return len(self._regions)

    def __getitem__(self, index: int) -> MemoryRegion:
        return self.regions[index]

    @property
    def regions(self) -> list[MemoryRegion]:
        """
        Return regions sorted by offset.
        """
        return sorted(self._regions)

    def add(self, region: MemoryRegion) -> None:
        """
        Add a region.
        """
        self._regions.append(region)

    def extend(self, regions: list[MemoryRegion]) -> None:
        """
        Add multiple regions.
        """
        self._regions.extend(regions)

    def clear(self) -> None:
        """
        Remove every region.
        """
        self._regions.clear()

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def find(self, offset: int) -> MemoryRegion | None:
        """
        Return the region containing an offset.
        """

        for region in self.regions:

            if offset in region:
                return region

        return None

    def by_kind(self, kind: str) -> list[MemoryRegion]:
        """
        Return every region of a given kind.
        """

        return [
            region
            for region in self.regions
            if region.kind == kind
        ]

    def overlapping(self) -> list[tuple[MemoryRegion, MemoryRegion]]:
        """
        Return overlapping regions.
        """

        overlaps = []

        regions = self.regions

        for current, nxt in zip(regions, regions[1:]):

            if current.overlaps(nxt):
                overlaps.append((current, nxt))

        return overlaps

    def gaps(self, filesize: int) -> list[tuple[int, int]]:
        """
        Return unclassified areas.

        Returns
        -------
        list[(offset, size)]
        """

        gaps = []

        current = 0

        for region in self.regions:

            if current < region.offset:

                gaps.append(
                    (
                        current,
                        region.offset - current,
                    )
                )

            current = max(current, region.end)

        if current < filesize:

            gaps.append(
                (
                    current,
                    filesize - current,
                )
            )

        return gaps

    # ------------------------------------------------------------------
    # Merge
    # ------------------------------------------------------------------

    def merge_adjacent(self) -> None:
        """
        Merge adjacent compatible regions.
        """

        regions = self.regions

        if not regions:
            return

        merged = []

        current = regions[0]

        for region in regions[1:]:

            if (
                current.kind == region.kind
                and current.adjacent(region)
            ):

                current = current.merge(region)

            else:

                merged.append(current)

                current = region

        merged.append(current)

        self._regions = merged

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def statistics(self) -> dict[str, int]:
        """
        Number of regions by kind.
        """

        stats: dict[str, int] = defaultdict(int)

        for region in self._regions:

            stats[region.kind] += 1

        return dict(stats)

    @property
    def total_size(self) -> int:
        """
        Total classified bytes.
        """

        return sum(region.size for region in self._regions)