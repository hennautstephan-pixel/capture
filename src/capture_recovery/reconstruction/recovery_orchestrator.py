from __future__ import annotations

from dataclasses import dataclass


from capture_recovery.reconstruction.corruption_analyzer import (
    CorruptionAnalyzer,
    CorruptionAnalysis,
)


from capture_recovery.reconstruction.reconstruction_strategy import (
    ReconstructionStrategy,
    ReconstructionDecision,
)


from capture_recovery.reconstruction.reconstruction_executor import (
    ReconstructionExecutor,
)



@dataclass(frozen=True, slots=True)
class RecoveryResult:
    """
    Complete recovery operation result.
    """

    success: bool

    data: bytes

    analysis: CorruptionAnalysis

    decisions: tuple[
        ReconstructionDecision,
        ...]



class RecoveryOrchestrator:
    """
    Coordinates the complete reconstruction flow.
    """



    def __init__(
        self,
        analyzer: CorruptionAnalyzer | None = None,
        strategy: ReconstructionStrategy | None = None,
        executor: ReconstructionExecutor | None = None,
    ) -> None:

        self._analyzer = (
            analyzer
            if analyzer is not None
            else CorruptionAnalyzer()
        )

        self._strategy = strategy

        self._executor = (
            executor
            if executor is not None
            else ReconstructionExecutor()
        )



    def recover(
        self,
        damaged: bytes,
        reference: bytes,
        *,
        object_type: str,
    ) -> RecoveryResult:
        """
        Execute a complete recovery.
        """

        analysis = self._analyzer.analyze(
            damaged,
            reference,
        )


        if self._strategy is None:

            raise ValueError(
                "A ReconstructionStrategy is required"
            )


        decisions = []


        repaired = damaged


        for region in analysis.regions:

            decision = self._strategy.build(
                region,

                object_type=object_type,
            )


            if decision is None:

                continue


            result = self._executor.execute(
                repaired,

                decision,
            )


            if result.success:

                repaired = result.data

                decisions.append(
                    decision
                )


        return RecoveryResult(
            success=(
                len(decisions)
                ==
                len(analysis.regions)
            ),

            data=repaired,

            analysis=analysis,

            decisions=tuple(
                decisions
            ),
        )