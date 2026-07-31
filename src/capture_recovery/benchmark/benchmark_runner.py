"""
Benchmark runner.
"""

from __future__ import annotations

from collections.abc import Callable

from .benchmark_result import BenchmarkResult
from .benchmark_statistics import BenchmarkStatistics
from .sample_loader import SampleLoader


class BenchmarkRunner:
    """
    Executes a benchmark over a collection of sample projects.
    """

    def __init__(
        self,
        loader: SampleLoader,
        analyser: Callable[[str], BenchmarkResult],
    ) -> None:

        self._loader = loader
        self._analyser = analyser

    @property
    def loader(self) -> SampleLoader:
        return self._loader

    @property
    def analyser(self) -> Callable[[str], BenchmarkResult]:
        return self._analyser

    def run(self) -> BenchmarkStatistics:
        """
        Execute the benchmark.
        """

        statistics = BenchmarkStatistics()

        for sample in self._loader:

            result = self._analyser(str(sample))

            statistics.add(result)

        return statistics