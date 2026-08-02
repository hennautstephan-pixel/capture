"""
Base classes for reconstruction heuristics.

A reconstruction heuristic analyses a damaged binary structure and proposes one
or more reconstruction candidates. It does not directly modify the recovery
pipeline; instead it returns scored candidates that can later be evaluated by
the reconstruction engine.

This module intentionally contains no Capture-specific logic. Concrete
heuristics are implemented in separate modules.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from .reconstruction_candidate import ReconstructionCandidate
from .reconstruction_context import ReconstructionContext


class ReconstructionHeuristic(ABC):
    """
    Base class for all reconstruction heuristics.

    Each heuristic is expected to analyse the current reconstruction context and
    yield zero or more reconstruction candidates.

    Implementations should never mutate the supplied context.
    """

    @property
    def name(self) -> str:
        """Human-readable heuristic name."""
        return self.__class__.__name__

    @abstractmethod
    def reconstruct(
        self,
        context: ReconstructionContext,
    ) -> Iterable[ReconstructionCandidate]:
        """
        Analyse the supplied context and yield reconstruction candidates.

        Parameters
        ----------
        context:
            Reconstruction context describing the damaged structure.

        Returns
        -------
        Iterable[ReconstructionCandidate]
            Zero or more possible reconstructions.
        """
        raise NotImplementedError

    def supports(
        self,
        context: ReconstructionContext,
    ) -> bool:
        """
        Indicates whether this heuristic is applicable to the supplied context.

        The default implementation always returns True.
        """

        return True


class NoOpReconstructionHeuristic(ReconstructionHeuristic):
    """
    Default heuristic used during infrastructure bring-up.

    It never proposes any reconstruction but validates that the reconstruction
    pipeline is operational.
    """

    def reconstruct(
        self,
        context: ReconstructionContext,
    ) -> Iterable[ReconstructionCandidate]:
        return ()