from __future__ import annotations

from dataclasses import dataclass

from .pattern_merger import (
    MergedPatternRegion,
    MergedPatterns,
)


@dataclass(slots=True, frozen=True)
class CandidateStructure:
    """
    Candidate binary structure.

    This is still a hypothesis.
    """

    offset: int

    length: int

    confidence: float

    evidence: tuple[str, ...]

    name: str | None = None

    @property
    def end(self) -> int:
        return self.offset + self.length


@dataclass(slots=True, frozen=True)
class StructureMap:
    """
    Candidate structures found inside
    the corpus.
    """

    structures: list[CandidateStructure]

    @property
    def structure_count(self) -> int:
        return len(self.structures)

    def by_offset(self) -> list[CandidateStructure]:
        """
        Return structures ordered by their
        position inside the binary file.
        """

        return sorted(
            self.structures,
            key=lambda structure: (
                structure.offset,
                structure.length,
            ),
        )


class StructureMapper:
    """
    Convert merged regions into candidate
    binary structures.

    No Capture-specific knowledge is used.

    Only objective observations.
    """

    def map(
        self,
        merged: MergedPatterns,
    ) -> StructureMap:

        structures: list[CandidateStructure] = []

        for region in merged.regions:

            structures.append(
                CandidateStructure(
                    offset=region.offset,
                    length=region.length,
                    confidence=self._confidence(region),
                    evidence=self._evidence(region),
                )
            )

        structures.sort(
            key=lambda structure: (
                -structure.confidence,
                structure.offset,
            ),
        )

        return StructureMap(structures)

    @staticmethod
    def _confidence(
        region: MergedPatternRegion,
    ) -> float:

        score = 0.0

        score += min(
            region.occurrence_count / 10.0,
            1.0,
        )

        score += min(
            region.source_region_count / 5.0,
            1.0,
        )

        return min(
            score / 2.0,
            1.0,
        )

    @staticmethod
    def _evidence(
        region: MergedPatternRegion,
    ) -> tuple[str, ...]:

        return (
            f"{region.occurrence_count} observations",
            f"{region.source_region_count} merged regions",
            f"length={region.length}",
        )