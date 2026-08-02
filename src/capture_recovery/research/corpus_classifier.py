from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.tools.diff_analyzer import DiffRegion

from .corpus_knowledge import (
    CorpusKnowledgeBase,
)


@dataclass(slots=True, frozen=True)
class ClassificationResult:
    """
    Result of corpus based classification.
    """

    category: str

    confidence: float

    evidence: tuple[str, ...]


class CorpusClassifier:
    """
    Classify binary difference regions using
    knowledge extracted from the reference corpus.
    """

    def classify(
        self,
        region: DiffRegion,
        knowledge_base: CorpusKnowledgeBase,
    ) -> ClassificationResult:
        """
        Find the closest known pattern.
        """

        if not knowledge_base.knowledge():

            return ClassificationResult(
                category="unknown",
                confidence=0.0,
                evidence=(
                    "No corpus knowledge available.",
                ),
            )

        best_category = "unknown"

        best_confidence = 0.0

        evidence = []

        for entry in knowledge_base.knowledge():

            confidence = self._compare(
                region,
                entry,
            )

            if confidence > best_confidence:

                best_category = entry.category

                best_confidence = confidence

                evidence = [
                    entry.description,
                ]

        return ClassificationResult(
            category=best_category,
            confidence=best_confidence,
            evidence=tuple(evidence),
        )


    def _compare(
        self,
        region: DiffRegion,
        entry,
    ) -> float:
        """
        Compare a region with a known corpus entry.

        Current model:
        compare only the size pattern.
        """

        description = entry.description.lower()

        size = region.size

        if "large" in description and size > 512:

            return min(
                entry.confidence,
                0.95,
            )

        if "small" in description and size < 64:

            return min(
                entry.confidence,
                0.75,
            )

        if size > 512:

            return entry.confidence * 0.8

        return 0.1