from __future__ import annotations

from capture_recovery.structures import Structure

from .inference_result import InferenceResult
from .inference_rule import InferenceRule


class InferenceEngine:
    """
    Executes inference rules and keeps the best match.
    """

    def __init__(
        self,
        rules: list[InferenceRule] | None = None,
    ) -> None:

        self._rules = rules or []

    def add_rule(
        self,
        rule: InferenceRule,
    ) -> None:

        self._rules.append(rule)

    def infer(
        self,
        structure: Structure,
    ) -> InferenceResult:

        best = InferenceResult(False)

        for rule in self._rules:

            result = rule.match(structure)

            if (
                result.matched
                and result.confidence > best.confidence
            ):
                best = result

        return best

    def infer_all(
        self,
        structures: list[Structure],
    ) -> list[InferenceResult]:

        return [
            self.infer(s)
            for s in structures
        ]