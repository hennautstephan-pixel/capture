from __future__ import annotations

from dataclasses import dataclass


from capture_recovery.reconstruction.object_library import (
    ObjectLibrary,
    LibraryObject,
)


from capture_recovery.reconstruction.candidate_ranker import (
    CandidateRanker,
)


from capture_recovery.reconstruction.corruption_analyzer import (
    CorruptionRegion,
)



@dataclass(frozen=True, slots=True)
class ReconstructionDecision:
    """
    Decision produced by reconstruction strategy.
    """

    offset: int

    size: int

    replacement: bytes

    object_type: str

    confidence: float

    source: str



class ReconstructionStrategy:
    """
    Selects the best replacement object
    for corrupted regions.
    """



    def __init__(
        self,
        library: ObjectLibrary,
        ranker: CandidateRanker | None = None,
    ) -> None:

        self._library = library

        self._ranker = (
            ranker
            if ranker is not None
            else CandidateRanker()
        )



    def build(
        self,
        region: CorruptionRegion,
        *,
        object_type: str,
        reference_data: bytes | None = None,
    ) -> ReconstructionDecision | None:
        """
        Create a reconstruction decision.
        """

        candidates = self._candidates(
            object_type,
        )


        if not candidates:

            return None



        candidate = self._ranker.best(
            tuple(candidates),

            object_type=object_type,

            size=region.size,

            reference_data=reference_data,
        )


        if candidate is None:

            return None



        confidence = self._confidence(
            candidate,

            region,
        )


        return ReconstructionDecision(
            offset=region.offset,

            size=region.size,

            replacement=candidate.data,

            object_type=candidate.object_type,

            confidence=confidence,

            source=candidate.source,
        )



    def _candidates(
        self,
        object_type: str,
    ) -> list[LibraryObject]:
        """
        Retrieve compatible objects.
        """

        return [
            obj
            for obj in self._library.objects
            if obj.object_type == object_type
        ]



    def _confidence(
        self,
        candidate: LibraryObject,
        region: CorruptionRegion,
    ) -> float:
        """
        Estimate reconstruction confidence.
        """

        if not candidate.data:

            return 0.0


        if len(candidate.data) == region.size:

            return 1.0


        difference = abs(
            len(candidate.data)
            -
            region.size
        )


        return max(
            0.0,

            1.0 -
            (
                difference /
                max(
                    len(candidate.data),
                    region.size,
                )
            ),
        )