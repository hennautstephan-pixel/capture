from __future__ import annotations

from dataclasses import dataclass

from .structure_candidate import StructureCandidate


@dataclass(slots=True, frozen=True)
class ScoreBreakdown:
    """
    Detailed scoring result.
    """

    alignment: float
    density: float
    confidence: float
    field_count: float
    total: float


class StructureScorer:
    """
    Compute a confidence score for a StructureCandidate.

    The current implementation intentionally relies only on structural
    information. Future versions may incorporate semantic knowledge,
    signatures and machine-learning based inference.
    """

    def __init__(
        self,
        *,
        alignment_weight: float = 20.0,
        density_weight: float = 30.0,
        confidence_weight: float = 30.0,
        field_weight: float = 20.0,
    ) -> None:

        self.alignment_weight = alignment_weight
        self.density_weight = density_weight
        self.confidence_weight = confidence_weight
        self.field_weight = field_weight

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def score(
        self,
        candidate: StructureCandidate,
    ) -> float:

        result = self.evaluate(candidate)

        candidate.score = result.total
        candidate.confidence = result.total

        return result.total

    def evaluate(
        self,
        candidate: StructureCandidate,
    ) -> ScoreBreakdown:

        alignment = (
            self._alignment_score(candidate)
            * self.alignment_weight
        )

        density = (
            self._density_score(candidate)
            * self.density_weight
        )

        confidence = (
            candidate.average_confidence
            * self.confidence_weight
        )

        field_count = (
            self._field_score(candidate)
            * self.field_weight
        )

        total = (
            alignment
            + density
            + confidence
            + field_count
        )

        total = max(
            0.0,
            min(
                total,
                100.0,
            ),
        )

        return ScoreBreakdown(
            alignment=alignment,
            density=density,
            confidence=confidence,
            field_count=field_count,
            total=total,
        )

    # ---------------------------------------------------------
    # Individual criteria
    # ---------------------------------------------------------

    @staticmethod
    def _alignment_score(
        candidate: StructureCandidate,
    ) -> float:

        offset = candidate.offset

        if offset % 16 == 0:
            return 1.0

        if offset % 8 == 0:
            return 0.8

        if offset % 4 == 0:
            return 0.6

        if offset % 2 == 0:
            return 0.4

        return 0.2

    @staticmethod
    def _density_score(
        candidate: StructureCandidate,
    ) -> float:

        return min(
            candidate.density,
            1.0,
        )

    @staticmethod
    def _field_score(
        candidate: StructureCandidate,
    ) -> float:

        count = candidate.field_count

        if count >= 32:
            return 1.0

        if count >= 16:
            return 0.8

        if count >= 8:
            return 0.6

        if count >= 4:
            return 0.4

        if count >= 2:
            return 0.2

        return 0.1

    # ---------------------------------------------------------
    # Callable
    # ---------------------------------------------------------

    def __call__(
        self,
        candidate: StructureCandidate,
    ) -> float:

        return self.score(candidate)