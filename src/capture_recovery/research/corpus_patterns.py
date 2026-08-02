from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .corpus_matrix import (
    CorpusMatrix,
    CorpusMatrixAnalyzer,
)


@dataclass(slots=True, frozen=True)
class PatternRegion:
    """
    One recurrent region found in the corpus.
    """

    offset: int

    length: int

    occurrence_count: int


@dataclass(slots=True)
class CorpusPatterns:
    """
    Collection of recurrent regions.
    """

    regions: list[PatternRegion]

    @property
    def pattern_count(self) -> int:
        return len(self.regions)

    def largest_region(self) -> PatternRegion | None:

        if not self.regions:
            return None

        return max(
            self.regions,
            key=lambda region: region.length,
        )

    def most_common_region(self) -> PatternRegion | None:

        if not self.regions:
            return None

        return max(
            self.regions,
            key=lambda region: region.occurrence_count,
        )


class CorpusPatternsAnalyzer:
    """
    Detect recurrent modified regions inside a corpus.

    This class is intentionally descriptive.
    It reports observed regions only and performs
    no heuristic merging.
    """

    def __init__(
        self,
        matrix: CorpusMatrixAnalyzer | None = None,
    ) -> None:

        self._matrix = (
            matrix
            or CorpusMatrixAnalyzer()
        )

    def analyze(
        self,
        directory: str | Path,
        pattern: str = "*.c2p",
    ) -> CorpusPatterns:

        matrix = self._matrix.analyze(
            directory,
            pattern,
        )

        return self.from_matrix(matrix)

    @classmethod
    def from_matrix(
        cls,
        matrix: CorpusMatrix,
    ) -> CorpusPatterns:

        counts = cls._count_regions(matrix)

        regions = sorted(
            (
                PatternRegion(
                    offset=offset,
                    length=length,
                    occurrence_count=count,
                )
                for (
                    offset,
                    length,
                ), count in counts.items()
            ),
            key=lambda region: (
                -region.occurrence_count,
                region.offset,
                region.length,
            ),
        )

        return CorpusPatterns(regions)

    @staticmethod
    def _count_regions(
        matrix: CorpusMatrix,
    ) -> dict[
        tuple[int, int],
        int,
    ]:

        counts: dict[
            tuple[int, int],
            int,
        ] = {}

        for entry in matrix.entries:

            for region in entry.difference.changed_regions:

                key = (
                    region.offset,
                    region.length,
                )

                counts[key] = (
                    counts.get(key, 0)
                    + 1
                )

        return counts