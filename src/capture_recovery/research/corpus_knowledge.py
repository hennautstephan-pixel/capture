from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class CorpusSample:
    """
    Reference sample stored in corpus.
    """

    name: str

    path: Path

    category: str


@dataclass(slots=True, frozen=True)
class CorpusKnowledgeEntry:
    """
    Knowledge extracted from corpus comparison.
    """

    category: str

    description: str

    confidence: float


class CorpusKnowledgeBase:
    """
    Knowledge database dedicated to corpus samples.

    Independent from the existing research KnowledgeBase.
    """

    def __init__(self) -> None:

        self._samples: list[CorpusSample] = []

        self._knowledge: list[CorpusKnowledgeEntry] = []


    def add_sample(
        self,
        sample: CorpusSample,
    ) -> None:

        self._samples.append(
            sample,
        )


    def add_knowledge(
        self,
        entry: CorpusKnowledgeEntry,
    ) -> None:

        self._knowledge.append(
            entry,
        )


    def samples(
        self,
    ) -> tuple[CorpusSample, ...]:

        return tuple(
            self._samples,
        )


    def knowledge(
        self,
    ) -> tuple[CorpusKnowledgeEntry, ...]:

        return tuple(
            self._knowledge,
        )


    def find_by_category(
        self,
        category: str,
    ) -> tuple[CorpusKnowledgeEntry, ...]:

        return tuple(
            item
            for item in self._knowledge
            if item.category == category
        )