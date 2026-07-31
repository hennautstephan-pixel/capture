from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from capture_recovery.knowledge.knowledge_base import KnowledgeSnapshot
from capture_recovery.knowledge.knowledge_inference_engine import InferenceReport, KnowledgeInferenceEngine
from capture_recovery.knowledge.knowledge_pipeline import KnowledgePipeline, KnowledgePipelineResult


@dataclass(frozen=True, slots=True)
class ExperimentResult:
    """Immutable result of one experiment over a single corpus entry."""

    source: str
    snapshot: KnowledgeSnapshot
    inference_report: InferenceReport


@dataclass(frozen=True, slots=True)
class CorpusExperimentReport:
    """Immutable aggregate report over an entire corpus execution."""

    experiments: tuple[ExperimentResult, ...]
    statistics: Mapping[str, int | float]


class CorpusExperimentRunner:
    """Coordinate the execution of a corpus through the knowledge pipeline.

    The runner is intentionally a thin orchestration layer. It does not inspect
    or interpret the resulting hypotheses and it never mutates the knowledge
    base or other dependencies.
    """

    def __init__(
        self,
        pipeline: KnowledgePipeline,
        inference_engine_factory: Callable[[KnowledgeSnapshot], KnowledgeInferenceEngine],
    ) -> None:
        self._pipeline = pipeline
        self._inference_engine_factory = inference_engine_factory

    def run(self, corpus: Mapping[str, bytes]) -> CorpusExperimentReport:
        """Run the full corpus through the knowledge pipeline and inference engine."""
        ordered_sources = tuple(sorted(corpus))
        experiments: list[ExperimentResult] = []

        for source in ordered_sources:
            payload = corpus[source]
            result = self._pipeline.build([payload])
            snapshot = result.snapshot
            inference_engine = self._inference_engine_factory(snapshot)
            inference_report = inference_engine.infer()
            experiments.append(
                ExperimentResult(
                    source=source,
                    snapshot=snapshot,
                    inference_report=inference_report,
                )
            )

        statistics = {
            "project_count": len(experiments),
            "total_inferences": sum(len(experiment.inference_report.inferences) for experiment in experiments),
            "total_knowledge_entries": sum(len(experiment.snapshot.entries) for experiment in experiments),
        }
        return CorpusExperimentReport(experiments=tuple(experiments), statistics=statistics)


__all__ = ["CorpusExperimentReport", "CorpusExperimentRunner", "ExperimentResult"]
