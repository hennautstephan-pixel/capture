from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .corpus_analyzer import CorpusAnalyzer


@dataclass(slots=True, frozen=True)
class CorpusStatistics:
    """
    Objective statistics collected from one Capture project.
    """

    path: Path

    file_size: int

    header_size: int

    compressed_size: int

    decompressed_size: int

    compression_ratio: float

    trailing_bytes: int


class CorpusStatisticsAnalyzer:
    """
    Produce objective statistics for one or more Capture
    project files.

    This class never attempts to interpret the Capture
    format. It only exposes measurable properties.
    """

    def __init__(
        self,
        analyzer: CorpusAnalyzer | None = None,
    ) -> None:

        self._analyzer = analyzer or CorpusAnalyzer()

    def analyze(
        self,
        path: str | Path,
    ) -> CorpusStatistics:

        analysis = self._analyzer.analyze(path)

        compressed = analysis.stream.compressed_size
        decompressed = analysis.stream.decompressed_size

        if compressed:
            ratio = decompressed / compressed
        else:
            ratio = 0.0

        return CorpusStatistics(
            path=analysis.path,
            file_size=analysis.file_size,
            header_size=analysis.header_size,
            compressed_size=compressed,
            decompressed_size=decompressed,
            compression_ratio=ratio,
            trailing_bytes=analysis.stream.trailing_bytes,
        )

    def analyze_directory(
        self,
        directory: str | Path,
        pattern: str = "*.c2p",
    ) -> list[CorpusStatistics]:

        directory = Path(directory)

        results: list[CorpusStatistics] = []

        for path in sorted(directory.glob(pattern)):
            results.append(
                self.analyze(path)
            )

        return results

    @staticmethod
    def average_compression_ratio(
        statistics: list[CorpusStatistics],
    ) -> float:

        if not statistics:
            return 0.0

        return (
            sum(
                item.compression_ratio
                for item in statistics
            )
            / len(statistics)
        )

    @staticmethod
    def total_compressed_size(
        statistics: list[CorpusStatistics],
    ) -> int:

        return sum(
            item.compressed_size
            for item in statistics
        )

    @staticmethod
    def total_decompressed_size(
        statistics: list[CorpusStatistics],
    ) -> int:

        return sum(
            item.decompressed_size
            for item in statistics
        )

    @staticmethod
    def largest_project(
        statistics: list[CorpusStatistics],
    ) -> CorpusStatistics | None:

        if not statistics:
            return None

        return max(
            statistics,
            key=lambda item: item.file_size,
        )