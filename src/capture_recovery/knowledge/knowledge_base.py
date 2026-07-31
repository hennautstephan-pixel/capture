from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Mapping

from capture_recovery.reverse.semantic_pattern_analyzer import PatternObservation, PatternReport


@dataclass(frozen=True, slots=True)
class KnowledgeEntry:
    """A single stored observation from a pattern report."""

    key: str
    observations: int
    confidence: float
    metadata: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class KnowledgeSnapshot:
    """A stable snapshot of the current knowledge base contents."""

    entries: tuple[KnowledgeEntry, ...]
    statistics: Mapping[str, int | float]


class KnowledgeBase:
    """Store and merge factual observations emitted by a pattern analyzer."""

    def __init__(self) -> None:
        """Initialize an empty knowledge base."""
        self._entries: dict[str, KnowledgeEntry] = {}

    def ingest(self, report: PatternReport) -> None:
        """Ingest a pattern report by merging each observation into the base.

        Observations are merged by their effective key, which is the
        ``pattern_id``. The occurrence counter is incremented, confidence is
        recomputed deterministically, and metadata is preserved in a stable
        form for later snapshots.
        """
        for observation in report.observations:
            self._merge_observation(observation)

    def snapshot(self) -> KnowledgeSnapshot:
        """Return a deterministic snapshot of the current knowledge base."""
        entries = tuple(
            sorted(self._entries.values(), key=lambda entry: entry.key)
        )
        statistics = {
            "entry_count": len(entries),
            "total_observations": sum(entry.observations for entry in entries),
            "average_confidence": (
                sum(entry.confidence for entry in entries) / len(entries)
                if entries
                else 0.0
            ),
        }
        return KnowledgeSnapshot(entries=entries, statistics=statistics)

    def query(self, key: str) -> KnowledgeEntry | None:
        """Return the stored entry for ``key`` when it exists."""
        return self._entries.get(key)

    def _merge_observation(self, observation: PatternObservation) -> None:
        existing = self._entries.get(observation.pattern_id)
        if existing is None:
            self._entries[observation.pattern_id] = KnowledgeEntry(
                key=observation.pattern_id,
                observations=1,
                confidence=self._confidence(observation),
                metadata=self._metadata(observation),
            )
            return

        merged_observations = existing.observations + 1
        merged_confidence = self._merge_confidence(existing.confidence, observation.confidence, merged_observations)
        merged_metadata = {
            **existing.metadata,
            **self._metadata(observation),
        }
        self._entries[observation.pattern_id] = KnowledgeEntry(
            key=observation.pattern_id,
            observations=merged_observations,
            confidence=merged_confidence,
            metadata=merged_metadata,
        )

    def _confidence(self, observation: PatternObservation) -> float:
        return max(0.0, min(1.0, observation.confidence))

    def _merge_confidence(self, previous: float, incoming: float, observations: int) -> float:
        weighted_confidence = ((previous * (observations - 1)) + incoming) / observations
        return max(0.0, min(1.0, weighted_confidence))

    def _metadata(self, observation: PatternObservation) -> dict[str, Any]:
        return {
            "description": observation.description,
            "value_type": observation.value_type,
            "offsets": observation.offsets,
            "occurrences": observation.occurrences,
        }


__all__ = ["KnowledgeBase", "KnowledgeEntry", "KnowledgeSnapshot"]
