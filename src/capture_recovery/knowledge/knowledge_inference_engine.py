from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from capture_recovery.knowledge.knowledge_base import KnowledgeEntry
from capture_recovery.knowledge.knowledge_query_engine import KnowledgeQueryEngine


@dataclass(frozen=True, slots=True)
class Inference:
    """An explicit hypothesis backed by evidence from the current knowledge snapshot."""

    subject: str
    hypothesis: str
    confidence: float
    evidence: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class InferenceReport:
    """Immutable report summarizing all generated inferences."""

    inferences: tuple[Inference, ...]
    statistics: Mapping[str, int | float]


class KnowledgeInferenceEngine:
    """Generate generic, deterministic hypotheses from consolidated knowledge.

    The engine is intentionally limited to objective observations already
    present in the knowledge base. It never mutates the base and does not try
    to attach domain-specific meaning to the evidence.
    """

    def __init__(self, query_engine: KnowledgeQueryEngine) -> None:
        self._query_engine = query_engine

    def infer(self) -> InferenceReport:
        """Generate deterministic hypotheses from the current knowledge snapshot."""
        entries = self._query_engine.top(limit=10).matches
        inferences = self._build_inferences(entries)
        return InferenceReport(
            inferences=inferences,
            statistics={
                "inference_count": len(inferences),
                "entry_count": len(entries),
                "max_confidence": max((inference.confidence for inference in inferences), default=0.0),
            },
        )

    def _build_inferences(self, entries: tuple[KnowledgeEntry, ...]) -> tuple[Inference, ...]:
        if not entries:
            return ()

        inferences: list[Inference] = []
        for entry in entries:
            if entry.observations >= 2:
                inferences.append(
                    self._repeated_observation_inference(entry)
                )
            if entry.confidence >= 0.7:
                inferences.append(
                    self._high_confidence_inference(entry)
                )
            if len(entries) >= 2:
                inferences.append(
                    self._group_presence_inference(entry)
                )

        return tuple(sorted(inferences, key=self._sort_key))

    def _repeated_observation_inference(self, entry: KnowledgeEntry) -> Inference:
        return Inference(
            subject=entry.key,
            hypothesis="repeated observations suggest a stable pattern",
            confidence=min(1.0, 0.5 + (entry.observations / 10.0)),
            evidence=(f"observations={entry.observations}", f"key={entry.key}"),
        )

    def _high_confidence_inference(self, entry: KnowledgeEntry) -> Inference:
        return Inference(
            subject=entry.key,
            hypothesis="high confidence indicates a strong signal",
            confidence=round(entry.confidence, 3),
            evidence=(f"confidence={entry.confidence:.3f}", f"key={entry.key}"),
        )

    def _group_presence_inference(self, entry: KnowledgeEntry) -> Inference:
        return Inference(
            subject=entry.key,
            hypothesis="presence in a grouped result set suggests a recurring profile",
            confidence=round(min(1.0, 0.3 + (entry.observations / 20.0)), 3),
            evidence=(f"observations={entry.observations}", f"key={entry.key}"),
        )

    def _sort_key(self, inference: Inference) -> tuple[str, float, tuple[str, ...]]:
        return (inference.subject, inference.confidence, inference.evidence)


__all__ = ["Inference", "InferenceReport", "KnowledgeInferenceEngine"]
