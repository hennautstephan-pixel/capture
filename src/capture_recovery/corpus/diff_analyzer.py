from __future__ import annotations

from dataclasses import dataclass

from .corpus_diff import (
    CorpusDiff,
    Difference,
)


@dataclass(slots=True, frozen=True)
class DifferenceRegion:
    """
    A contiguous region of differences.
    """

    start: int

    end: int

    differences: tuple[Difference, ...]

    @property
    def size(self) -> int:
        return self.end - self.start + 1

    @property
    def count(self) -> int:
        return len(self.differences)


@dataclass(slots=True, frozen=True)
class AnalysisReport:
    """
    Result of a corpus difference analysis.
    """

    regions: tuple[DifferenceRegion, ...]

    @property
    def region_count(self) -> int:
        return len(self.regions)

    @property
    def difference_count(self) -> int:
        return sum(
            region.count
            for region in self.regions
        )


class DiffAnalyzer:
    """
    Analyse corpus differences by grouping
    contiguous difference locations.
    """

    def analyze(
        self,
        diff: CorpusDiff,
    ) -> AnalysisReport:

        if not diff.differences:
            return AnalysisReport(
                regions=(),
            )

        regions: list[DifferenceRegion] = []

        current: list[Difference] = []

        start = 0
        end = 0

        for index, difference in enumerate(diff.differences):

            if not current:

                current.append(difference)

                start = index
                end = index

                continue

            if index == end + 1:

                current.append(difference)

                end = index

                continue

            regions.append(
                DifferenceRegion(
                    start=start,
                    end=end,
                    differences=tuple(current),
                )
            )

            current = [difference]

            start = index
            end = index

        regions.append(
            DifferenceRegion(
                start=start,
                end=end,
                differences=tuple(current),
            )
        )

        return AnalysisReport(
            regions=tuple(regions),
        )