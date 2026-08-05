from __future__ import annotations

from dataclasses import dataclass


from capture_recovery.reconstruction.object_library import (
    LibraryObject,
)


from capture_recovery.reconstruction.binary_similarity import (
    BinarySimilarity,
)



@dataclass(frozen=True, slots=True)
class CandidateScore:
    """
    Score assigned to a reconstruction candidate.
    """

    candidate: LibraryObject

    score: float



class CandidateRanker:
    """
    Ranks reconstruction candidates.

    Scoring:

    - object type match
    - size match
    - binary similarity
    """



    def __init__(
        self,
        similarity: BinarySimilarity | None = None,
    ) -> None:

        self._similarity = (
            similarity
            if similarity is not None
            else BinarySimilarity()
        )



    def rank(
        self,
        candidates: tuple[LibraryObject, ...],
        *,
        object_type: str | None = None,
        size: int | None = None,
        reference_data: bytes | None = None,
    ) -> tuple[CandidateScore, ...]:
        """
        Rank candidates from best to worst.
        """

        scored = []


        for candidate in candidates:

            scored.append(
                CandidateScore(
                    candidate=candidate,

                    score=self._score(
                        candidate,

                        object_type=object_type,

                        size=size,

                        reference_data=reference_data,
                    ),
                )
            )


        return tuple(
            sorted(
                scored,

                key=lambda item: item.score,

                reverse=True,
            )
        )



    def best(
        self,
        candidates: tuple[LibraryObject, ...],
        *,
        object_type: str | None = None,
        size: int | None = None,
        reference_data: bytes | None = None,
    ) -> LibraryObject | None:
        """
        Return best candidate.
        """

        ranked = self.rank(
            candidates,

            object_type=object_type,

            size=size,

            reference_data=reference_data,
        )


        if not ranked:

            return None


        return ranked[0].candidate



    def _score(
        self,
        candidate: LibraryObject,
        *,
        object_type: str | None,
        size: int | None,
        reference_data: bytes | None,
    ) -> float:
        """
        Compute candidate score.
        """

        score = 0.0


        if object_type is not None:

            if candidate.object_type == object_type:

                score += 0.5



        if size is not None:

            if len(candidate.data) == size:

                score += 0.3



        if reference_data is not None:

            score += (
                self._similarity.score(
                    candidate.data,

                    reference_data,
                )
                * 0.2
            )


        return score