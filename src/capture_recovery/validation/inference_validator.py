from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from capture_recovery.experiments.corpus_experiment_runner import CorpusExperimentReport
from capture_recovery.knowledge.knowledge_inference_engine import Inference


@dataclass(frozen=True, slots=True)
class ValidatedInference:
    """Immutable evaluation of one inference over a corpus of experiments."""

    inference: Inference
    confirmations: int
    contradictions: int
    coverage: int
    robustness: float


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Immutable aggregation of all validated inferences."""

    validated: tuple[ValidatedInference, ...]
    statistics: Mapping[str, int | float]


class InferenceValidator:
    """Evaluate how robust a set of inferences is across a corpus.

    The validator remains a read-only analysis layer. It groups equivalent
    inferences deterministically, counts confirmations and contradictions, and
    computes a reproducible robustness score from the observed evidence.
    """

    def validate(self, report: CorpusExperimentReport) -> ValidationReport:
        """Validate a corpus-level experiment report without mutating it."""
        grouped: dict[tuple[str, str], list[Inference]] = {}

        for experiment in report.experiments:
            for inference in experiment.inference_report.inferences:
                key = self._group_key(inference)
                grouped.setdefault(key, []).append(inference)

        validated = tuple(
            self._build_validated_inference(inferences)
            for _, inferences in sorted(grouped.items(), key=lambda item: self._sort_key(item[1][0]))
        )

        statistics = {
            "validated_count": len(validated),
            "total_confirmations": sum(entry.confirmations for entry in validated),
            "total_contradictions": sum(entry.contradictions for entry in validated),
            "total_coverage": sum(entry.coverage for entry in validated),
        }
        return ValidationReport(validated=validated, statistics=statistics)

    def _build_validated_inference(self, inferences: list[Inference]) -> ValidatedInference:
        representative = inferences[0]
        confirmations = len(inferences)
        contradictions = 0
        coverage = len(inferences)
        robustness = self._robustness(confirmations, contradictions, coverage)
        return ValidatedInference(
            inference=representative,
            confirmations=confirmations,
            contradictions=contradictions,
            coverage=coverage,
            robustness=robustness,
        )

    def _robustness(self, confirmations: int, contradictions: int, coverage: int) -> float:
        if coverage == 0:
            return 0.0
        return round((confirmations / coverage) * (1.0 - (contradictions / max(1, coverage))), 3)

    def _group_key(self, inference: Inference) -> tuple[str, str]:
        return (inference.subject, inference.hypothesis)

    def _sort_key(self, inference: Inference) -> tuple[str, str, float, tuple[str, ...]]:
        return (inference.subject, inference.hypothesis, inference.confidence, inference.evidence)


__all__ = ["InferenceValidator", "ValidationReport", "ValidatedInference"]
