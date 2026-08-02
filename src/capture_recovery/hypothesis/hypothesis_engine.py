from __future__ import annotations

from capture_recovery.structures import (
    StructureCandidate,
)

from .hypothesis_result import HypothesisResult
from .rule_engine import RuleEngine


class HypothesisEngine:
    """
    High-level semantic inference engine.

    The engine itself contains no inference rules.

    It simply delegates inference to RuleEngine.
    """

    def __init__(
        self,
        rule_engine: RuleEngine | None = None,
    ) -> None:

        self._rule_engine = (
            rule_engine
            if rule_engine is not None
            else RuleEngine()
        )

    @property
    def rule_engine(self) -> RuleEngine:

        return self._rule_engine

    def infer(
        self,
        candidate: StructureCandidate,
    ) -> HypothesisResult:

        return self._rule_engine.apply(
            candidate,
        )

    def __call__(
        self,
        candidate: StructureCandidate,
    ) -> HypothesisResult:

        return self.infer(
            candidate,
        )