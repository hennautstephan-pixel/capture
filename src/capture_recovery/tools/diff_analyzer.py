from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.tools.diff_stream import (
    StreamDiff,
    StreamDifference,
)


@dataclass(slots=True, frozen=True)
class DiffRegion:
    """
    Continuous region of differences.
    """

    start_offset: int

    end_offset: int

    differences: tuple[StreamDifference, ...]

    @property
    def size(self) -> int:
        """
        Number of bytes in this region.
        """

        return (
            self.end_offset
            - self.start_offset
            + 1
        )


@dataclass(slots=True, frozen=True)
class DiffAnalysis:
    """
    Analysis result of a stream diff.
    """

    regions: tuple[DiffRegion, ...]

    @property
    def region_count(self) -> int:
        return len(self.regions)


class DiffAnalyzer:
    """
    Analyze binary differences and group them
    into continuous regions.
    """

    def analyze(
        self,
        diff: StreamDiff,
    ) -> DiffAnalysis:
        """
        Convert byte differences into regions.
        """

        if diff.identical:

            return DiffAnalysis(
                regions=(),
            )

        sorted_differences = sorted(
            diff.differences,
            key=lambda item: item.offset,
        )

        regions = []

        current = [
            sorted_differences[0],
        ]

        for difference in sorted_differences[1:]:

            previous = current[-1]

            if difference.offset <= previous.offset + 1:

                current.append(
                    difference,
                )

            else:

                regions.append(
                    self._create_region(
                        current,
                    )
                )

                current = [
                    difference,
                ]

        regions.append(
            self._create_region(
                current,
            )
        )

        return DiffAnalysis(
            regions=tuple(regions),
        )

    def _create_region(
        self,
        differences: list[StreamDifference],
    ) -> DiffRegion:

        return DiffRegion(
            start_offset=differences[0].offset,
            end_offset=differences[-1].offset,
            differences=tuple(differences),
        )