"""
Property discovery result.
"""

from __future__ import annotations

from dataclasses import dataclass

from .property_candidate import PropertyCandidate


@dataclass(
    frozen=True,
    slots=True,
)
class DiscoveryResult:
    """
    Result produced by the PropertyDiscoveryEngine.
    """

    candidates: tuple[PropertyCandidate, ...] = ()

    analysed_diffs: int = 0

    @property
    def discovered_properties(self) -> int:
        """
        Number of discovered properties.
        """
        return len(self.candidates)

    @property
    def is_empty(self) -> bool:
        """
        True if no property was discovered.
        """
        return not self.candidates

    @property
    def has_candidates(self) -> bool:
        """
        True if at least one candidate exists.
        """
        return bool(self.candidates)