"""
Header recovery heuristic.

Uses HeaderScanner to locate known binary headers and produces
reconstruction candidates.

The heuristic never modifies the binary buffer.
It only proposes possible recovery points.
"""

from __future__ import annotations

from typing import Iterable

from .header_scanner import HeaderScanner
from .heuristic import ReconstructionHeuristic
from .reconstruction_candidate import ReconstructionCandidate
from .reconstruction_context import ReconstructionContext


class HeaderRecoveryHeuristic(ReconstructionHeuristic):
    """
    Detect known headers inside a damaged binary stream.
    """

    def __init__(
        self,
        scanner: HeaderScanner,
    ) -> None:
        self._scanner = scanner

    @property
    def scanner(self) -> HeaderScanner:
        return self._scanner

    def supports(
        self,
        context: ReconstructionContext,
    ) -> bool:
        """
        A header can only be searched inside
        a non-empty binary buffer.
        """

        return context.size > 0

    def reconstruct(
        self,
        context: ReconstructionContext,
    ) -> Iterable[ReconstructionCandidate]:
        """
        Search every registered header and
        return one candidate for each occurrence.
        """

        results = self._scanner.scan(context.data)

        for result in results:

            score = result.confidence

            # Slight bonus for headers aligned on
            # a 4-byte boundary.
            if result.offset % 4 == 0:
                score = min(1.0, score + 0.05)

            yield ReconstructionCandidate(
                score=score,
                heuristic=self.name,
                description=(
                    f"Recovered header "
                    f"'{result.signature.name}' "
                    f"at offset {result.offset}"
                ),
                modifications={
                    "header_name": result.signature.name,
                    "header_offset": result.offset,
                    "header_size": result.signature.size,
                },
                metadata={
                    "alignment": result.offset % 4,
                },
            )