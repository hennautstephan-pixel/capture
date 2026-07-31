from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from capture_recovery.knowledge.knowledge_base import KnowledgeBase, KnowledgeEntry


@dataclass(frozen=True, slots=True)
class QueryResult:
    """Immutable result produced by a read-only knowledge query."""

    query: str
    matches: tuple[KnowledgeEntry, ...]
    statistics: Mapping[str, int | float]


class KnowledgeQueryEngine:
    """Execute objective, deterministic queries over a KnowledgeBase.

    The engine deliberately stays in the read-only query layer. It never
    mutates the underlying knowledge base and does not infer any business
    semantics from the stored observations.
    """

    def __init__(self, knowledge_base: KnowledgeBase) -> None:
        self._knowledge_base = knowledge_base

    def by_key(self, key: str) -> QueryResult:
        """Return the exact entry matching ``key`` when it exists.

        Results are sorted by key to keep the order deterministic and stable.
        """
        matches = tuple(
            sorted(
                (entry for entry in self._iter_entries() if entry.key == key),
                key=self._sort_key,
            )
        )
        return QueryResult(
            query=key,
            matches=matches,
            statistics=self._build_statistics(matches, query_type="by_key"),
        )

    def by_prefix(self, prefix: str) -> QueryResult:
        """Return entries whose key starts with ``prefix``.

        Ordering is deterministic: shorter keys are considered first, then the
        natural key order is used as a tie-breaker.
        """
        matches = tuple(
            sorted(
                (entry for entry in self._iter_entries() if entry.key.startswith(prefix)),
                key=self._sort_key,
            )
        )
        return QueryResult(
            query=prefix,
            matches=matches,
            statistics=self._build_statistics(matches, query_type="by_prefix"),
        )

    def by_confidence(self, minimum: float) -> QueryResult:
        """Return entries whose confidence is greater than or equal to ``minimum``."""
        matches = tuple(
            sorted(
                (entry for entry in self._iter_entries() if entry.confidence >= minimum),
                key=self._sort_key,
            )
        )
        return QueryResult(
            query=str(minimum),
            matches=matches,
            statistics=self._build_statistics(matches, query_type="by_confidence"),
        )

    def top(self, limit: int = 10) -> QueryResult:
        """Return the most frequently observed entries, capped by ``limit``.

        The ordering is deterministic: entries with more observations come first,
        then the key order is used as a stable tie-breaker.
        """
        if limit < 0:
            raise ValueError("limit must be non-negative")

        matches = tuple(
            sorted(
                self._iter_entries(),
                key=lambda entry: (-entry.observations, entry.key),
            )[:limit]
        )
        return QueryResult(
            query=str(limit),
            matches=matches,
            statistics=self._build_statistics(matches, query_type="top"),
        )

    def statistics(self) -> Mapping[str, int | float]:
        """Return aggregate statistics for the underlying knowledge base."""
        entries = tuple(self._iter_entries())
        return {
            "entry_count": len(entries),
            "total_observations": sum(entry.observations for entry in entries),
            "average_confidence": (
                sum(entry.confidence for entry in entries) / len(entries)
                if entries
                else 0.0
            ),
        }

    def _iter_entries(self) -> tuple[KnowledgeEntry, ...]:
        snapshot = self._knowledge_base.snapshot()
        return snapshot.entries

    def _build_statistics(self, matches: tuple[KnowledgeEntry, ...], query_type: str) -> Mapping[str, int | float]:
        return {
            "query_type": query_type,
            "match_count": len(matches),
            "returned_count": len(matches),
            "entry_count": len(self._iter_entries()),
        }

    def _sort_key(self, entry: KnowledgeEntry) -> tuple[int, str, int, float]:
        return (len(entry.key), entry.key, entry.observations, entry.confidence)


__all__ = ["KnowledgeQueryEngine", "QueryResult"]
