from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from capture_recovery.recovery.intelligent_recovery_pipeline import (
    IntelligentRecoveryPipeline,
)

from capture_recovery.reconstruction.reconstruction_planner import (
    ReconstructionPlanner,
    ReconstructionPlan,
)

from capture_recovery.reconstruction.reconstruction_executor import (
    ReconstructionExecutor,
)

from capture_recovery.reconstruction.object_library import (
    ObjectLibrary,
)

from capture_recovery.recovery.intelligent_restore_action import (
    IntelligentRestoreAction,
)


@dataclass(slots=True, frozen=True)
class FullRecoveryResult:
    """
    Complete recovery result.
    """

    source: Path

    output: Path

    plans: tuple[ReconstructionPlan, ...]

    restored_objects: int



class FullRecoveryPipeline:
    """
    Complete Capture recovery workflow.

    Pipeline:

    analysis
        ->
    reconstruction planning
        ->
    binary execution
    """

    def __init__(
        self,
        *,
        object_library: ObjectLibrary,
    ) -> None:

        self._analysis = (
            IntelligentRecoveryPipeline()
        )

        self._planner = (
            ReconstructionPlanner(
                object_library,
            )
        )

        self._executor = (
            ReconstructionExecutor()
        )



    def recover(
        self,
        *,
        diff,
        knowledge_base,
        source: Path,
        output: Path,
    ) -> FullRecoveryResult:
        """
        Execute complete recovery.
        """

        analysis = (
            self._analysis.analyze(
                diff,
                knowledge_base,
            )
        )


        actions = getattr(
            analysis,
            "actions",
            (),
        )


        plans = []


        for action in actions:

            if not isinstance(
                action,
                IntelligentRestoreAction,
            ):
                continue


            plan = self._planner.plan(
                action,
            )


            if plan is not None:

                plans.append(
                    plan,
                )


        if plans:

            self._executor.execute_many(
                tuple(plans),
                source,
                output,
            )


        return FullRecoveryResult(
            source=source,
            output=output,
            plans=tuple(plans),
            restored_objects=len(plans),
        )