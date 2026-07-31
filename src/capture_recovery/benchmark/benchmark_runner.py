"""
Benchmark runner.
"""

from __future__ import annotations

from collections.abc import Callable

from .benchmark_result import BenchmarkResult
from .benchmark_session import BenchmarkSession
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

    def run_session(self) -> BenchmarkSession:
        """
        Execute the benchmark and return a complete session.
        """

        session = BenchmarkSession(
            samples_directory=self.loader.root,
        )

        for sample in self.loader:

            result = self._analyser(
                str(sample),
            )

            session.statistics.add(
                result,
            )

        session.finish()

        return session

    def run(self) -> BenchmarkStatistics:
        """
        Backward compatible API.

        Returns benchmark statistics.
        """

        return self.run_session().statistics