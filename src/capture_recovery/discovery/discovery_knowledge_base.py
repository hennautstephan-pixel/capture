"""
Discovery knowledge base.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Dict

from .knowledge_entry import KnowledgeEntry
from .property_candidate import PropertyCandidate


class DiscoveryKnowledgeBase:
    """Stores discovered properties across analyses."""

    def __init__(self) -> None:
        self._entries: Dict[str, KnowledgeEntry] = {}

    def add(self, candidate: PropertyCandidate) -> KnowledgeEntry:
        entry = KnowledgeEntry.from_candidate(candidate)
        existing = self._entries.get(entry.identifier)
        if existing is None:
            self._entries[entry.identifier] = entry
            return entry
        updated = existing.confirm(candidate)
        self._entries[entry.identifier] = updated
        return updated

    def add_entry(self, entry: KnowledgeEntry) -> None:
        self._entries[entry.identifier] = entry

    def merge(self, other: "DiscoveryKnowledgeBase") -> None:
        for entry in other:
            existing = self._entries.get(entry.identifier)
            if existing is None:
                self._entries[entry.identifier] = entry
            else:
                self._entries[entry.identifier] = KnowledgeEntry(
                    object_type=existing.object_type,
                    property_name=existing.property_name,
                    offset=existing.offset,
                    value_type=existing.value_type,
                    confidence=(existing.confidence + entry.confidence) / 2.0,
                    observations=existing.observations + entry.observations,
                    confirmations=existing.confirmations + entry.confirmations,
                    contradictions=existing.contradictions + entry.contradictions,
                )

    def find(self, identifier: str) -> KnowledgeEntry | None:
        return self._entries.get(identifier)

    def by_object(self, object_type: str):
        return tuple(e for e in self._entries.values() if e.object_type == object_type)

    def by_name(self, property_name: str):
        return tuple(e for e in self._entries.values() if e.property_name == property_name)

    def by_offset(self, offset: int):
        return tuple(e for e in self._entries.values() if e.offset == offset)

    @property
    def total_entries(self) -> int:
        return len(self._entries)

    @property
    def confirmed_entries(self) -> int:
        return sum(e.is_confirmed for e in self._entries.values())

    @property
    def total_observations(self) -> int:
        return sum(e.observations for e in self._entries.values())

    @property
    def average_confidence(self) -> float:
        if not self._entries:
            return 0.0
        return sum(e.confidence for e in self._entries.values()) / len(self._entries)

    def __contains__(self, identifier: str) -> bool:
        return identifier in self._entries

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self) -> Iterator[KnowledgeEntry]:
        return iter(self._entries.values())