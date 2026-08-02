from __future__ import annotations

from dataclasses import dataclass

from .corpus_patterns import (
    CorpusPatterns,
    PatternRegion,
)


@dataclass(slots=True, frozen=True)
class MergedPatternRegion:
    """
    Region produced by merging several observed regions.
    """

    offset: int

    length: int

    occurrence_count: int

    merged_regions: tuple[
        PatternRegion,
        ...,
    ]

    @property
    def end(self) -> int:
        return self.offset + self.length

    @property
    def source_region_count(self) -> int:
        """
        Number of original regions contributing
        to this merged region.
        """
        return len(self.merged_regions)


@dataclass(slots=True, frozen=True)
class MergedPatterns:
    """
    Result of the pattern merging process.
    """

    regions: list[MergedPatternRegion]

    @property
    def region_count(self) -> int:
        return len(self.regions)


class PatternMerger:
    """
    Merge overlapping or adjacent pattern regions.

    This class is intentionally heuristic.

    It never modifies the original observations.
    """

    def merge(
        self,
        patterns: CorpusPatterns,
        *,
        max_gap: int = 0,
    ) -> MergedPatterns:

        if not patterns.regions:
            return MergedPatterns([])

        ordered = sorted(
            patterns.regions,
            key=lambda region: (
                region.offset,
                region.length,
            ),
        )

        merged: list[MergedPatternRegion] = []

        current: list[PatternRegion] = [
            ordered[0]
        ]

        current_start = ordered[0].offset

        current_end = (
            ordered[0].offset
            + ordered[0].length
        )

        for region in ordered[1:]:

            region_start = region.offset

            region_end = (
                region.offset
                + region.length
            )

            if (
                region_start
                <= current_end + max_gap
            ):

                current.append(region)

                current_end = max(
                    current_end,
                    region_end,
                )

                continue

            merged.append(
                self._build_region(
                    current,
                    current_start,
                    current_end,
                )
            )

            current = [region]

            current_start = region.offset

            current_end = region_end

        merged.append(
            self._build_region(
                current,
                current_start,
                current_end,
            )
        )

        return MergedPatterns(merged)

    @staticmethod
    def _build_region(
        regions: list[PatternRegion],
        start: int,
        end: int,
    ) -> MergedPatternRegion:

        return MergedPatternRegion(
            offset=start,
            length=end - start,
            occurrence_count=sum(
                region.occurrence_count
                for region in regions
            ),
            merged_regions=tuple(regions),
        )