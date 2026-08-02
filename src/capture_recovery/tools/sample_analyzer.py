from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from capture_recovery.corpus import (
    CorpusBuilder,
    CorpusDiffer,
)
from capture_recovery.tools.compare_all import (
    CompareAll,
)


@dataclass(slots=True, frozen=True)
class SampleStatistics:
    """
    Global statistics about a sample corpus.
    """

    file_count: int
    comparison_count: int
    identical_pairs: int
    different_pairs: int


@dataclass(slots=True, frozen=True)
class SampleReport:
    """
    Complete analysis report.
    """

    statistics: SampleStatistics

    comparisons: tuple


class SampleAnalyzer:
    """
    Analyse every Capture sample in a directory.
    """

    def __init__(self) -> None:

        self._builder = CorpusBuilder()

        self._differ = CorpusDiffer()

        self._compare_all = CompareAll()

    def analyze(
        self,
        directory: str | Path,
    ) -> SampleReport:

        corpus = self._builder.build(directory)

        report = self._compare_all.compare(directory)

        statistics = SampleStatistics(
            file_count=corpus.count,
            comparison_count=report.comparison_count,
            identical_pairs=report.identical_pairs,
            different_pairs=report.different_pairs,
        )

        return SampleReport(
            statistics=statistics,
            comparisons=report.comparisons,
        )