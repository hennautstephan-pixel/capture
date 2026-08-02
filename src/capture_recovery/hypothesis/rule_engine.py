from __future__ import annotations

from typing import Iterable

from capture_recovery.structures import (
    StructureCandidate,
)

from .hypothesis import Hypothesis
from .hypothesis_result import HypothesisResult
from .rule import HypothesisRule
from .rules import ScoreRule


class RuleEngine:
    """
    Execute a collection of hypothesis rules.

    The engine itself contains no inference logic.
    It simply delegates to the registered rules.

    If no rule produces a hypothesis, an "Unknown"
    hypothesis is generated.
    """

    def __init__(
        self,
        rules: Iterable[HypothesisRule] | None = None,
    ) -> None:

        if rules is None:
            rules = (
                ScoreRule(),
            )

        self._rules = sorted(
            list(rules),
            key=lambda r: r.priority,
            reverse=True,
        )

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def rules(self) -> tuple[HypothesisRule, ...]:

        return tuple(self._rules)

    @property
    def count(self) -> int:

        return len(self._rules)

    # ---------------------------------------------------------
    # Rule management
    # ---------------------------------------------------------

    def add(
        self,
        rule: HypothesisRule,
    ) -> None:

        self._rules.append(rule)

        self._rules.sort(
            key=lambda r: r.priority,
            reverse=True,
        )

    def clear(self) -> None:

        self._rules.clear()

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------

    def _fallback(
        self,
        candidate: StructureCandidate,
    ) -> Hypothesis:

        return Hypothesis(
            object_type="Unknown",
            confidence=max(
                5.0,
                candidate.score * 0.5,
            ),
            candidate=candidate,
            source="fallback",
        )

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def apply(
        self,
        candidate: StructureCandidate,
    ) -> HypothesisResult:

        hypotheses: list[Hypothesis] = []

        for rule in self._rules:

            hypotheses.extend(
                rule.apply(
                    candidate,
                )
            )

        #
        # Always return at least one hypothesis.
        #

        if not hypotheses:

            hypotheses.append(
                self._fallback(
                    candidate,
                )
            )

        return HypothesisResult(
            hypotheses=hypotheses,
        )

    # ---------------------------------------------------------
    # Callable
    # ---------------------------------------------------------

    def __call__(
        self,
        candidate: StructureCandidate,
    ) -> HypothesisResult:

        return self.apply(
            candidate,
        )