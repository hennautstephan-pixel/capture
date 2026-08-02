from __future__ import annotations

from capture_recovery.structures import (
    StructureCandidate,
)

from .. import Hypothesis
from ..rule import HypothesisRule


class ScoreRule(HypothesisRule):
    """
    Produce hypotheses according to the structural score.
    """

    @property
    def name(self) -> str:

        return "score"

    @property
    def priority(self) -> int:

        return 100

    def apply(
        self,
        candidate: StructureCandidate,
    ) -> list[Hypothesis]:

        if candidate.score >= 90:

            return [
                Hypothesis(
                    object_type="Structure",
                    confidence=min(
                        candidate.score,
                        99.0,
                    ),
                    candidate=candidate,
                    source=self.name,
                )
            ]

        if candidate.score >= 75:

            return [
                Hypothesis(
                    object_type="PossibleStructure",
                    confidence=candidate.score,
                    candidate=candidate,
                    source=self.name,
                )
            ]

        return []