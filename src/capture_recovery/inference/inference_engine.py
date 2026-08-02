from __future__ import annotations

from typing import Any

from capture_recovery.knowledge import KnowledgeResult
from capture_recovery.structures import Structure

from .inference_context import InferenceContext
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
        *,
        knowledge_result: KnowledgeResult | None = None,
        project: Any = None,
        options: dict[str, Any] | None = None,
    ) -> InferenceResult:
        """
        Execute every inference rule against a structure.

        A shared InferenceContext is created once and passed to every
        rule so they can access project information, knowledge results
        and future recovery services.
        """

        context = InferenceContext(
            structure=structure,
            knowledge_result=knowledge_result,
            project=project,
            options=options or {},
        )

        best = InferenceResult(False)

        for rule in self._rules:

            result = rule.match(context)

            if (
                result.matched
                and result.confidence > best.confidence
            ):
                best = result

        return best

    def infer_all(
        self,
        structures: list[Structure],
        *,
        knowledge_result: KnowledgeResult | None = None,
        project: Any = None,
        options: dict[str, Any] | None = None,
    ) -> list[InferenceResult]:
        """
        Execute inference on every structure.
        """

        return [
            self.infer(
                structure,
                knowledge_result=knowledge_result,
                project=project,
                options=options,
            )
            for structure in structures
        ]