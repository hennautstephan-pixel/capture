from __future__ import annotations

from dataclasses import dataclass, field

from .field_mapper import (
    FieldMap,
)


@dataclass(slots=True, frozen=True)
class KnowledgeEntry:
    """
    One knowledge entry extracted from the corpus.
    """

    offset: int

    length: int

    type_candidates: tuple[str, ...]

    confidence: float

    evidence: tuple[str, ...]

    semantic_name: str | None = None

    description: str | None = None

    @property
    def end(self) -> int:
        return self.offset + self.length


@dataclass(slots=True)
class KnowledgeBase:
    """
    Collection of discovered knowledge.
    """

    entries: list[KnowledgeEntry] = field(
        default_factory=list
    )

    def __iter__(self):

        return iter(self.entries)

    def __len__(self) -> int:

        return len(self.entries)

    def add(
        self,
        entry: KnowledgeEntry,
    ) -> None:

        self.entries.append(entry)

    @property
    def entry_count(self) -> int:

        return len(self.entries)

    def by_offset(
        self,
    ) -> list[KnowledgeEntry]:

        return sorted(
            self.entries,
            key=lambda entry: (
                entry.offset,
                entry.length,
            ),
        )

    def by_confidence(
        self,
    ) -> list[KnowledgeEntry]:

        return sorted(
            self.entries,
            key=lambda entry: (
                -entry.confidence,
                entry.offset,
            ),
        )

    def highest_confidence(
        self,
    ) -> KnowledgeEntry | None:

        if not self.entries:
            return None

        return max(
            self.entries,
            key=lambda entry: entry.confidence,
        )

    def find(
        self,
        offset: int,
    ) -> KnowledgeEntry | None:

        for entry in self.entries:

            if entry.offset == offset:
                return entry

        return None

    def find_name(
        self,
        semantic_name: str,
    ) -> KnowledgeEntry | None:

        for entry in self.entries:

            if entry.semantic_name == semantic_name:
                return entry

        return None

    def find_type(
        self,
        type_name: str,
    ) -> list[KnowledgeEntry]:

        return [
            entry
            for entry in self.entries
            if type_name in entry.type_candidates
        ]


class KnowledgeBaseBuilder:
    """
    Build a knowledge base from candidate fields.

    This builder records observations only.
    Semantic names may be assigned later by
    dedicated correlators.
    """

    def build(
        self,
        fields: FieldMap,
    ) -> KnowledgeBase:

        kb = KnowledgeBase()

        for field in fields.by_offset():

            kb.add(
                KnowledgeEntry(
                    offset=field.offset,
                    length=field.length,
                    type_candidates=field.type_candidates,
                    confidence=field.confidence,
                    evidence=field.evidence,
                    semantic_name=field.name,
                )
            )

        return kb