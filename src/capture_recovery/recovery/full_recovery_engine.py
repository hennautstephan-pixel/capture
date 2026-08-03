from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from capture_recovery.recovery.intelligent_recovery_pipeline import (
    IntelligentRecoveryPipeline,
)

from capture_recovery.recovery.binary_repair_executor import (
    BinaryRepairExecutor,
    BinaryExecutionResult,
)

from capture_recovery.research.corpus_knowledge import (
    CorpusKnowledgeBase,
)


@dataclass(slots=True, frozen=True)
class RecoveryReport:
    """
    Final recovery report.
    """

    source: Path

    output: Path

    executed_actions: int

    skipped_actions: int

    binary_result: BinaryExecutionResult | None



class FullRecoveryEngine:
    """
    Complete intelligent recovery engine.

    Workflow:

    - analyse differences
    - generate repair plan
    - execute binary repairs
    - return recovery report

    The original file is never modified.
    """

    def __init__(
        self,
        *,
        minimum_confidence: float = 0.80,
    ) -> None:

        self._pipeline = (
            IntelligentRecoveryPipeline(
                minimum_confidence=minimum_confidence,
            )
        )

        self._binary_executor = (
            BinaryRepairExecutor()
        )


    def repair(
        self,
        *,
        diff,
        knowledge_base: CorpusKnowledgeBase,
        source: Path,
        output: Path,
        project=None,
        report=None,
        replacements: tuple[bytes, ...] = (),
    ) -> RecoveryReport:
        """
        Execute a complete intelligent recovery.

        Binary replacements are supplied externally
        until the object reconstruction layer exists.
        """


        analysis = self._pipeline.analyze(
            diff,
            knowledge_base,
        )


        plan = self._pipeline.prepare(
            analysis,
        )


        binary_result = None


        if replacements:

            binary_result = (
                self._binary_executor.execute_plan(
                    plan.actions,
                    source,
                    output,
                    replacements,
                )
            )


        return RecoveryReport(
            source=source,
            output=output,
            executed_actions=(
                len(binary_result.actions)
                if binary_result
                else 0
            ),
            skipped_actions=0,
            binary_result=binary_result,
        )