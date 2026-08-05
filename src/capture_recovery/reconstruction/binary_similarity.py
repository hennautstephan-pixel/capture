from __future__ import annotations

from dataclasses import dataclass



@dataclass(frozen=True, slots=True)
class SimilarityResult:
    """
    Result of binary comparison.
    """

    score: float

    compared_bytes: int

    matching_bytes: int



class BinarySimilarity:
    """
    Binary data similarity analyzer.

    Produces a normalized score:

    0.0 -> completely different
    1.0 -> identical
    """



    def compare(
        self,
        left: bytes,
        right: bytes,
    ) -> SimilarityResult:
        """
        Compare two binary sequences.
        """

        if not left and not right:

            return SimilarityResult(
                score=1.0,

                compared_bytes=0,

                matching_bytes=0,
            )


        if not left or not right:

            return SimilarityResult(
                score=0.0,

                compared_bytes=0,

                matching_bytes=0,
            )


        length = min(
            len(left),
            len(right),
        )


        matches = 0


        for index in range(length):

            if left[index] == right[index]:

                matches += 1


        score = (
            matches /
            max(
                len(left),
                len(right),
            )
        )


        return SimilarityResult(
            score=score,

            compared_bytes=length,

            matching_bytes=matches,
        )



    def score(
        self,
        left: bytes,
        right: bytes,
    ) -> float:
        """
        Shortcut returning only score.
        """

        return self.compare(
            left,
            right,
        ).score



    def identical(
        self,
        left: bytes,
        right: bytes,
    ) -> bool:
        """
        Check exact equality.
        """

        return left == right