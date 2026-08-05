from __future__ import annotations

from dataclasses import dataclass


from capture_recovery.reconstruction.object_library import (
    ObjectLibrary,
    LibraryObject,
)


from capture_recovery.recovery.intelligent_restore_action import (
    IntelligentRestoreAction,
)



@dataclass(frozen=True, slots=True)
class ReconstructionPlan:
    """
    Result of a reconstruction decision.

    Keeps compatibility with existing
    reconstruction pipeline.
    """

    offset: int

    size: int

    object_type: str

    replacement: bytes

    source: str

    confidence: float

    object: LibraryObject | None = None


    @property
    def data(
        self,
    ) -> bytes:
        """
        Compatibility alias.
        """

        return self.replacement



class ReconstructionPlanner:
    """
    Creates reconstruction plans from
    restoration actions.

    Uses candidate ranking when available.
    """



    def __init__(
        self,
        library: ObjectLibrary,
        ranker=None,
    ) -> None:

        self._library = library

        self._ranker = ranker



    def plan(
        self,
        action: IntelligentRestoreAction,
    ) -> ReconstructionPlan | None:
        """
        Create a reconstruction plan.
        """

        candidate = self._find_candidate(
            action,
        )


        if candidate is None:

            return None


        return ReconstructionPlan(
            offset=action.offset,

            size=action.size,

            object_type=candidate.object_type,

            replacement=candidate.data,

            source=candidate.source,

            confidence=action.confidence,

            object=candidate,
        )



    def _find_candidate(
        self,
        action: IntelligentRestoreAction,
    ) -> LibraryObject | None:
        """
        Find best reconstruction candidate.

        Priority:

        1. CandidateRanker
        2. Historical ObjectLibrary.find()
        """

        candidates = [
            obj
            for obj in self._library.objects
            if obj.object_type == action.object_type
        ]


        if candidates:

            if self._ranker is None:

                from capture_recovery.reconstruction.candidate_ranker import (
                    CandidateRanker,
                )

                self._ranker = CandidateRanker()


            ranked = self._ranker.best(
                tuple(candidates),

                object_type=action.object_type,

                size=action.size,
            )


            if ranked is not None:

                return ranked



        return self._library.find(
            object_type=action.object_type,

            size=action.size,
        )