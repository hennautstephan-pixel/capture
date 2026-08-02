from __future__ import annotations

from typing import Protocol

from capture_recovery.structures import (
    StructureCandidate,
)

from .hypothesis import Hypothesis


class HypothesisRule(Protocol):
    """
    Protocol implemented by every hypothesis rule.

    A rule analyses a StructureCandidate and returns zero,
    one or several semantic hypotheses.

    Rules are intentionally stateless and independent so they
    can easily be combined inside RuleEngine.
    """

    @property
    def name(self) -> str:
        """
        Human-readable rule name.
        """
        ...

    @property
    def priority(self) -> int:
        """
        Execution priority.

        Higher priority rules are evaluated first.
        """
        ...

    def apply(
        self,
        candidate: StructureCandidate,
    ) -> list[Hypothesis]:
        """
        Produce semantic hypotheses.

        Parameters
        ----------
        candidate:
            StructureCandidate being analysed.

        Returns
        -------
        list[Hypothesis]
            Possibly empty list of hypotheses.
        """
        ...