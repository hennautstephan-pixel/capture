"""
Registry of reconstruction heuristics.

The registry is responsible for:

- registering heuristics;
- executing compatible heuristics;
- collecting reconstruction candidates;
- returning candidates ordered by confidence.

It deliberately performs no Capture-specific logic. Its only responsibility is
to orchestrate heuristics.
"""

from __future__ import annotations

from typing import Iterable

from .heuristic import ReconstructionHeuristic
from .reconstruction_candidate import ReconstructionCandidate
from .reconstruction_context import ReconstructionContext


class ReconstructionRegistry:
    """
    Registry and execution engine for reconstruction heuristics.
    """

    def __init__(self) -> None:
        self._heuristics: list[ReconstructionHeuristic] = []

    @property
    def heuristics(self) -> tuple[ReconstructionHeuristic, ...]:
        """
        Registered heuristics.
        """
        return tuple(self._heuristics)

    def register(
        self,
        heuristic: ReconstructionHeuristic,
    ) -> None:
        """
        Register a reconstruction heuristic.

        Duplicate heuristic classes are ignored.
        """

        for existing in self._heuristics:
            if type(existing) is type(heuristic):
                return

        self._heuristics.append(heuristic)

    def unregister(
        self,
        heuristic_type: type[ReconstructionHeuristic],
    ) -> None:
        """
        Remove a heuristic from the registry.
        """

        self._heuristics = [
            heuristic
            for heuristic in self._heuristics
            if not isinstance(heuristic, heuristic_type)
        ]

    def clear(self) -> None:
        """
        Remove all registered heuristics.
        """

        self._heuristics.clear()

    def run(
        self,
        context: ReconstructionContext,
    ) -> list[ReconstructionCandidate]:
        """
        Execute every compatible heuristic.

        Returns
        -------
        list[ReconstructionCandidate]
            Candidates ordered by decreasing score.
        """

        candidates: list[ReconstructionCandidate] = []

        for heuristic in self._heuristics:

            if not heuristic.supports(context):
                continue

            produced = heuristic.reconstruct(context)

            if produced is None:
                continue

            candidates.extend(produced)

        candidates.sort(
            key=lambda candidate: candidate.score,
            reverse=True,
        )

        return candidates

    def best(
        self,
        context: ReconstructionContext,
    ) -> ReconstructionCandidate | None:
        """
        Return the best reconstruction candidate.
        """

        candidates = self.run(context)

        if not candidates:
            return None

        return candidates[0]

    def __len__(self) -> int:
        return len(self._heuristics)

    def __iter__(self) -> Iterable[ReconstructionHeuristic]:
        return iter(self._heuristics)