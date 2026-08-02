from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.tools.diff_analyzer import (
    DiffAnalysis,
    DiffRegion,
)


@dataclass(slots=True, frozen=True)
class ObjectCandidate:
    """
    Possible object detected from a binary difference.
    """

    offset: int

    size: int

    object_type: str

    confidence: float

    reason: str


@dataclass(slots=True, frozen=True)
class ObjectIdentification:
    """
    Result of object identification.
    """

    candidates: tuple[ObjectCandidate, ...]

    @property
    def candidate_count(self) -> int:
        return len(self.candidates)


class ObjectIdentifier:
    """
    Identify possible Capture objects from
    binary difference regions.
    """

    def identify(
        self,
        analysis: DiffAnalysis,
    ) -> ObjectIdentification:
        """
        Convert diff regions into object candidates.
        """

        candidates = []

        for region in analysis.regions:

            candidates.append(
                self._identify_region(
                    region,
                )
            )

        return ObjectIdentification(
            candidates=tuple(candidates),
        )

    def _identify_region(
        self,
        region: DiffRegion,
    ) -> ObjectCandidate:
        """
        Apply initial heuristics.

        Current rules:
        - small region:
          likely property change
        - medium region:
          possible object update
        - large region:
          possible object insertion
        """

        size = region.size

        if size < 16:

            object_type = "property"

            confidence = 0.40

            reason = (
                "Small binary modification, "
                "possibly a property value."
            )

        elif size < 512:

            object_type = "object_field_block"

            confidence = 0.60

            reason = (
                "Medium binary region, "
                "possibly structured object data."
            )

        else:

            object_type = "object"

            confidence = 0.75

            reason = (
                "Large binary region, "
                "possible object insertion "
                "or complex structure."
            )

        return ObjectCandidate(
            offset=region.start_offset,
            size=size,
            object_type=object_type,
            confidence=confidence,
            reason=reason,
        )