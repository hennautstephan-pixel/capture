from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from capture_recovery.research.corpus_classifier import (
    CorpusClassifier,
)

from capture_recovery.tools.diff_analyzer import (
    DiffAnalysis,
    DiffRegion,
)


if TYPE_CHECKING:

    from capture_recovery.research.corpus_knowledge import (
        CorpusKnowledgeBase,
    )


@dataclass(slots=True, frozen=True)
class IntelligentObjectCandidate:
    """
    Object candidate enriched with corpus knowledge.
    """

    offset: int

    size: int

    object_type: str

    confidence: float

    evidence: tuple[str, ...]


@dataclass(slots=True, frozen=True)
class IntelligentObjectIdentification:
    """
    Result of intelligent identification.
    """

    candidates: tuple[IntelligentObjectCandidate, ...]

    @property
    def candidate_count(self) -> int:
        return len(self.candidates)


class IntelligentObjectIdentifier:
    """
    Object identifier using corpus knowledge.
    """

    def __init__(self) -> None:

        self._classifier = CorpusClassifier()


    def identify(
        self,
        analysis: DiffAnalysis,
        knowledge_base: CorpusKnowledgeBase,
    ) -> IntelligentObjectIdentification:
        """
        Identify objects from diff regions.
        """

        candidates = []

        for region in analysis.regions:

            candidates.append(
                self._identify_region(
                    region,
                    knowledge_base,
                )
            )

        return IntelligentObjectIdentification(
            candidates=tuple(candidates),
        )


    def _identify_region(
        self,
        region: DiffRegion,
        knowledge_base: CorpusKnowledgeBase,
    ) -> IntelligentObjectCandidate:

        classification = self._classifier.classify(
            region,
            knowledge_base,
        )

        return IntelligentObjectCandidate(
            offset=region.start_offset,
            size=region.size,
            object_type=classification.category,
            confidence=classification.confidence,
            evidence=classification.evidence,
        )