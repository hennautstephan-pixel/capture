from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.recovery.intelligent_restore_action import (
    IntelligentRestoreAction,
)

from capture_recovery.recovery.intelligent_repair_engine import (
    IntelligentRepairCandidate,
    IntelligentRepairResult,
)


@dataclass(slots=True, frozen=True)
class AdaptedRepairPlan:
    """
    Repair actions ready for the existing recovery engine.
    """

    actions: tuple[RepairAction, ...]


class IntelligentRepairAdapter:
    """
    Convert intelligent repair candidates into
    existing RepairAction objects.
    """

    def adapt(
        self,
        result: IntelligentRepairResult,
    ) -> AdaptedRepairPlan:
        """
        Convert an intelligent repair result
        into executable repair actions.
        """

        actions = tuple(
            self._convert_candidate(
                candidate,
            )
            for candidate in result.candidates
        )

        return AdaptedRepairPlan(
            actions=actions,
        )


    def _convert_candidate(
        self,
        candidate: IntelligentRepairCandidate,
    ) -> IntelligentRestoreAction:

        return IntelligentRestoreAction(
            offset=candidate.offset,
            size=candidate.size,
            object_type=candidate.object_type,
            confidence=candidate.confidence,
        )