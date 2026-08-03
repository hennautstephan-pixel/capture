from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.recovery.intelligent_repair_engine import (
    IntelligentRepairEngine,
    IntelligentRepairResult,
)

from capture_recovery.recovery.intelligent_repair_adapter import (
    IntelligentRepairAdapter,
    AdaptedRepairPlan,
)

from capture_recovery.recovery.intelligent_repair_executor import (
    IntelligentRepairExecutor,
    IntelligentExecutionResult,
)

from capture_recovery.research.corpus_knowledge import (
    CorpusKnowledgeBase,
)



@dataclass(slots=True, frozen=True)
class IntelligentRecoveryResult:
    """
    Complete result of intelligent recovery workflow.
    """

    analysis: IntelligentRepairResult

    plan: AdaptedRepairPlan

    execution: IntelligentExecutionResult



class IntelligentRecoveryPipeline:
    """
    High level orchestration pipeline.

    Connects:

    - intelligent analysis
    - repair adaptation
    - controlled execution

    No binary writing is performed here.
    """

    def __init__(
        self,
        *,
        minimum_confidence: float = 0.80,
    ) -> None:

        self._repair_engine = (
            IntelligentRepairEngine()
        )

        self._adapter = (
            IntelligentRepairAdapter()
        )

        self._executor = (
            IntelligentRepairExecutor(
                minimum_confidence=minimum_confidence,
            )
        )


    def analyze(
        self,
        diff,
        knowledge_base: CorpusKnowledgeBase,
    ) -> IntelligentRepairResult:
        """
        Run intelligent analysis only.
        """

        return self._repair_engine.analyze(
            diff,
            knowledge_base,
        )


    def prepare(
        self,
        analysis: IntelligentRepairResult,
    ) -> AdaptedRepairPlan:
        """
        Convert intelligent candidates
        into executable repair actions.
        """

        return self._adapter.adapt(
            analysis,
        )


    def execute(
        self,
        plan: AdaptedRepairPlan,
        project,
        report,
    ) -> IntelligentExecutionResult:
        """
        Execute a prepared repair plan.
        """

        return self._executor.execute(
            plan,
            project,
            report,
        )


    def run(
        self,
        diff,
        knowledge_base: CorpusKnowledgeBase,
        project,
        report,
    ) -> IntelligentRecoveryResult:
        """
        Execute the complete intelligent
        recovery workflow.
        """

        analysis = self.analyze(
            diff,
            knowledge_base,
        )


        plan = self.prepare(
            analysis,
        )


        execution = self.execute(
            plan,
            project,
            report,
        )


        return IntelligentRecoveryResult(
            analysis=analysis,
            plan=plan,
            execution=execution,
        )