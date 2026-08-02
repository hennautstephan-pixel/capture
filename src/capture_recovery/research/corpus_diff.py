from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .corpus_analyzer import CorpusAnalyzer


@dataclass(slots=True, frozen=True)
class DifferenceRegion:
    offset: int
    length: int


@dataclass(slots=True, frozen=True)
class CorpusDifference:
    left: Path
    right: Path

    compressed_equal: bool
    decompressed_equal: bool

    changed_regions: list[DifferenceRegion]


class CorpusDiff:
    """
    Compare two Capture projects.

    The comparison is intentionally based on the
    decompressed stream.
    """

    def __init__(
        self,
        analyzer: CorpusAnalyzer | None = None,
    ) -> None:
        self._analyzer = analyzer or CorpusAnalyzer()

    def compare(
        self,
        left: str | Path,
        right: str | Path,
    ) -> CorpusDifference:

        left_analysis = self._analyzer.analyze(left)
        right_analysis = self._analyzer.analyze(right)

        left_data = left_analysis.stream.decompressed
        right_data = right_analysis.stream.decompressed

        compressed_equal = (
            left_analysis.stream.compressed_size
            == right_analysis.stream.compressed_size
        )

        decompressed_equal = left_data == right_data

        changed_regions: list[DifferenceRegion] = []

        region_start: int | None = None

        common_length = min(
            len(left_data),
            len(right_data),
        )

        for offset in range(common_length):

            if left_data[offset] != right_data[offset]:

                if region_start is None:
                    region_start = offset

            elif region_start is not None:

                changed_regions.append(
                    DifferenceRegion(
                        offset=region_start,
                        length=offset - region_start,
                    )
                )

                region_start = None

        if region_start is not None:
            changed_regions.append(
                DifferenceRegion(
                    offset=region_start,
                    length=common_length - region_start,
                )
            )

        #
        # One stream is longer than the other.
        #
        if len(left_data) != len(right_data):

            changed_regions.append(
                DifferenceRegion(
                    offset=common_length,
                    length=abs(
                        len(left_data) - len(right_data)
                    ),
                )
            )

        return CorpusDifference(
            left=Path(left),
            right=Path(right),
            compressed_equal=compressed_equal,
            decompressed_equal=decompressed_equal,
            changed_regions=changed_regions,
        )