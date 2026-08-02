from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from capture_recovery.tools.diff_stream import (
    StreamDiffer,
)

from capture_recovery.tools.stream_sample_loader import (
    StreamSampleLoader,
)


@dataclass(slots=True, frozen=True)
class Comparison:

    left: Path

    right: Path

    diff: object


@dataclass(slots=True, frozen=True)
class ComparisonReport:

    comparisons: tuple

    @property
    def comparison_count(self) -> int:

        return len(self.comparisons)

    @property
    def identical_pairs(self) -> int:

        return sum(
            comparison.diff.identical
            for comparison in self.comparisons
        )

    @property
    def different_pairs(self) -> int:

        return (
            self.comparison_count
            - self.identical_pairs
        )


class CompareAll:
    """
    Compare decompressed Capture streams.
    """

    def __init__(self) -> None:

        self._loader = StreamSampleLoader()

        self._differ = StreamDiffer()


    def compare(
        self,
        directory: str | Path,
    ) -> ComparisonReport:

        directory = Path(directory)

        files = sorted(
            file
            for file in directory.iterdir()
            if file.is_file()
        )

        streams = {}

        for file in files:

            try:
                streams[file] = self._loader.load(
                    file,
                )

            except Exception:
                streams[file] = file.read_bytes()

        comparisons = []

        for index, left in enumerate(files):

            for right in files[index + 1:]:

                diff = self._differ.compare(
                    streams[left],
                    streams[right],
                )

                comparisons.append(
                    Comparison(
                        left=left,
                        right=right,
                        diff=diff,
                    )
                )

        return ComparisonReport(
            comparisons=tuple(comparisons),
        )