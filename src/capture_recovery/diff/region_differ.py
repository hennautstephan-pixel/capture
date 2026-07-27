"""
Region differ.

Groups BinaryChange objects by MemoryRegion.
"""

from __future__ import annotations

from collections import defaultdict

from capture_recovery.memory.memory_map import MemoryMap

from .models import BinaryChange
from .models import RegionChange


class RegionDiffer:
    """
    Groups BinaryChange objects by MemoryRegion.
    """

    def compare(
        self,
        changes: tuple[BinaryChange, ...],
        memory_map: MemoryMap,
    ) -> tuple[RegionChange, ...]:
        """
        Associate every BinaryChange with its MemoryRegion.

        Parameters
        ----------
        changes
            Binary changes produced by BinaryDiffer.

        memory_map
            Memory map describing the file.

        Returns
        -------
        tuple[RegionChange, ...]
        """

        grouped: dict[int, list[BinaryChange]] = defaultdict(list)
        regions: dict[int, object] = {}

        for change in changes:

            region = memory_map.find(change.offset)

            if region is None:
                continue

            key = id(region)

            grouped[key].append(change)
            regions[key] = region

        result: list[RegionChange] = []

        for key, binary_changes in grouped.items():

            region = regions[key]

            result.append(
                RegionChange(
                    offset=region.offset,
                    region=region,
                    binary_changes=tuple(
                        sorted(
                            binary_changes,
                            key=lambda c: c.offset,
                        )
                    ),
                )
            )

        result.sort(key=lambda r: r.offset)

        return tuple(result)

    def compare_report(
        self,
        changes: tuple[BinaryChange, ...],
        memory_map: MemoryMap,
    ) -> tuple[RegionChange, ...]:
        """
        Compatibility wrapper.
        """

        return self.compare(changes, memory_map)