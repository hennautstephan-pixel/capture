from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.research.corpus_knowledge import (
    CorpusKnowledgeBase,
)

from capture_recovery.tools.diff_analyzer import (
    DiffAnalyzer,
)

from capture_recovery.tools.intelligent_object_identifier import (
    IntelligentObjectIdentifier,
)


@dataclass(slots=True, frozen=True)
class IntelligentRepairCandidate:
    """
    A repair candidate generated from corpus knowledge.
    """

    object_type: str

    offset: int

    size: int

    confidence: float

    evidence: tuple[str, ...]


@dataclass(slots=True, frozen=True)
class IntelligentRepairPlan:
    """
    Non destructive repair proposal.
    """

    candidates: tuple[
        IntelligentRepairCandidate,
        ...
    ]


@dataclass(slots=True, frozen=True)
class IntelligentRepairResult:
    """
    Result of intelligent repair analysis.
    """

    candidates: tuple[
        IntelligentRepairCandidate,
        ...
    ]

    repair_plan: IntelligentRepairPlan



class IntelligentRepairEngine:
    """
    Recovery engine using corpus based identification.

    This version only analyses and proposes repairs.
    It does not modify binary data.
    """

    def __init__(self) -> None:

        self._diff_analyzer = DiffAnalyzer()

        self._identifier = (
            IntelligentObjectIdentifier()
        )


    def analyze(
        self,
        diff,
        knowledge_base: CorpusKnowledgeBase,
    ) -> IntelligentRepairResult:
        """
        Analyse a difference and generate
        a repair proposal.
        """

        analysis = self._diff_analyzer.analyze(
            diff,
        )

        identification = (
            self._identifier.identify(
                analysis,
                knowledge_base,
            )
        )


        candidates = tuple(
            self._convert_candidate(
                candidate,
            )
            for candidate
            in identification.candidates
        )


        return IntelligentRepairResult(
            candidates=candidates,
            repair_plan=IntelligentRepairPlan(
                candidates=candidates,
            ),
        )


    def _convert_candidate(
        self,
        candidate,
    ) -> IntelligentRepairCandidate:

        return IntelligentRepairCandidate(
            object_type=candidate.object_type,
            offset=candidate.offset,
            size=candidate.size,
            confidence=candidate.confidence,
            evidence=candidate.evidence,
        )