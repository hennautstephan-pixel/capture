"""
Correlation protocol.
"""

from __future__ import annotations

from typing import Protocol, Sequence

from .property_candidate import PropertyCandidate
from .property_observation import PropertyObservation


class Correlation(Protocol):
    """
    Protocol implemented by all property correlators.
    """

    PRIORITY: int = 0

    @property
    def priority(self) -> int:
        """
        Execution priority.

        Correlators having a higher priority are executed before
        lower priority correlators.
        """
        return self.PRIORITY

    def analyse(
        self,
        observations: Sequence[PropertyObservation],
    ) -> PropertyCandidate | None:
        """
        Analyse a collection of observations and return a discovered
        property candidate.

        Returns None if no reliable candidate can be inferred.
        """
        ...