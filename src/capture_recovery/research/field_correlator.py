from __future__ import annotations

from dataclasses import dataclass

from .knowledge_base import (
    KnowledgeBase,
)


@dataclass(slots=True, frozen=True)
class FieldCorrelation:
    """
    Correlation describing one candidate field.
    """

    offset: int

    length: int

    confidence: float

    type_candidates: tuple[str, ...]

    evidence: tuple[str, ...]

    occurrence_count: int

    semantic_name: str | None = None

    @property
    def end(self) -> int:
        return self.offset + self.length

    @property
    def is_unique(self) -> bool:
        """
        Convenience helper.

        A field is unique if it appears exactly once
        in the knowledge base.
        """
        return self.occurrence_count == 1


@dataclass(slots=True, frozen=True)
class CorrelationReport:
    """
    Result of the field correlation process.
    """

    correlations: list[FieldCorrelation]

    @property
    def correlation_count(self) -> int:
        return len(self.correlations)

    def by_offset(self) -> list[FieldCorrelation]:

        return sorted(
            self.correlations,
            key=lambda correlation: (
                correlation.offset,
                correlation.length,
            ),
        )

    def by_confidence(self) -> list[FieldCorrelation]:

        return sorted(
            self.correlations,
            key=lambda correlation: (
                -correlation.confidence,
                correlation.offset,
            ),
        )


class FieldCorrelator:
    """
    Produce simple correlations from the knowledge base.

    This class intentionally performs only objective
    correlations.

    It does not attempt to infer Capture semantics.
    """

    def correlate(
        self,
        knowledge: KnowledgeBase,
    ) -> CorrelationReport:

        counts: dict[
            tuple[int, int],
            int,
        ] = {}

        for entry in knowledge:

            key = (
                entry.offset,
                entry.length,
            )

            counts[key] = (
                counts.get(key, 0)
                + 1
            )

        correlations: list[
            FieldCorrelation
        ] = []

        for entry in knowledge.by_offset():

            key = (
                entry.offset,
                entry.length,
            )

            correlations.append(
                FieldCorrelation(
                    offset=entry.offset,
                    length=entry.length,
                    confidence=entry.confidence,
                    type_candidates=entry.type_candidates,
                    evidence=entry.evidence,
                    occurrence_count=counts[key],
                    semantic_name=entry.semantic_name,
                )
            )

        return CorrelationReport(
            correlations
        )