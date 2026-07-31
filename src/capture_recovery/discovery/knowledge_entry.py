"""
Knowledge entry.
"""

from __future__ import annotations

from dataclasses import dataclass

from .property_candidate import PropertyCandidate
from .value_type import ValueType


@dataclass(frozen=True, slots=True)
class KnowledgeEntry:
    """
    Represents a discovered property stored in the knowledge base.
    """

    object_type: str

    property_name: str

    offset: int

    value_type: ValueType

    confidence: float

    observations: int

    confirmations: int

    contradictions: int

    @property
    def identifier(self) -> str:
        """
        Unique identifier.
        """
        return (
            f"{self.object_type}:"
            f"{self.offset}:"
            f"{self.property_name}"
        )

    @property
    def is_confirmed(self) -> bool:
        """
        Returns True if the entry has never been contradicted.
        """
        return self.contradictions == 0

    @property
    def confidence_percent(self) -> float:
        """
        Confidence expressed as a percentage.
        """
        return self.confidence * 100.0

    @classmethod
    def from_candidate(
        cls,
        candidate: PropertyCandidate,
    ) -> "KnowledgeEntry":
        """
        Creates a knowledge entry from a discovered candidate.
        """
        return cls(
            object_type=candidate.object_type,
            property_name=candidate.property_name,
            offset=candidate.offset,
            value_type=candidate.value_type,
            confidence=candidate.confidence,
            observations=candidate.observations,
            confirmations=1,
            contradictions=0,
        )

    def confirm(
        self,
        candidate: PropertyCandidate,
    ) -> "KnowledgeEntry":
        """
        Returns a new entry updated with an additional confirmation.
        """
        total = self.confirmations + 1

        confidence = (
            (self.confidence * self.confirmations)
            + candidate.confidence
        ) / total

        return KnowledgeEntry(
            object_type=self.object_type,
            property_name=self.property_name,
            offset=self.offset,
            value_type=self.value_type,
            confidence=confidence,
            observations=(
                self.observations
                + candidate.observations
            ),
            confirmations=total,
            contradictions=self.contradictions,
        )

    def contradict(self) -> "KnowledgeEntry":
        """
        Returns a new entry updated after a contradiction.
        """
        total = self.confirmations + self.contradictions + 1

        confidence = (
            self.confidence
            * (self.confirmations / total)
        )

        return KnowledgeEntry(
            object_type=self.object_type,
            property_name=self.property_name,
            offset=self.offset,
            value_type=self.value_type,
            confidence=confidence,
            observations=self.observations,
            confirmations=self.confirmations,
            contradictions=self.contradictions + 1,
        )