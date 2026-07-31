"""
Benchmark analyser.

Adapter between the recovery pipeline and the benchmark
framework.
"""

from __future__ import annotations

from capture_recovery.pipeline import FullRecoveryPipeline

from .benchmark_result import BenchmarkResult


class BenchmarkAnalyser:
    """
    Adapts FullRecoveryPipeline to the BenchmarkRunner API.
    """

    def __init__(
        self,
        pipeline: FullRecoveryPipeline | None = None,
    ) -> None:

        self._pipeline = (
            pipeline
            or FullRecoveryPipeline()
        )

    @property
    def pipeline(self) -> FullRecoveryPipeline:
        """
        Underlying recovery pipeline.
        """

        return self._pipeline

    def __call__(
        self,
        path: str,
    ) -> BenchmarkResult:
        """
        Analyse a Capture project and return a
        BenchmarkResult.
        """

        analysis = self._pipeline.analyse(
            path,
        )

        return BenchmarkResult.from_analysis(
            analysis,
        )