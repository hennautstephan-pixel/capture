from __future__ import annotations

from dataclasses import dataclass

from typing import Any

from capture_recovery.recovery.repair_action import (
    RepairAction,
    RepairResult,
)


@dataclass(slots=True, frozen=True)
class IntelligentRestoreAction(
    RepairAction
):
    """
    Repair action generated from intelligent analysis.

    This action represents a proposed object restoration.
    """

    offset: int

    size: int

    object_type: str

    confidence: float

    priority: int = 100


    @property
    def action_type(self) -> str:
        """
        Compatibility identifier used by adapters/tests.
        """

        return "restore_object"


    def execute(
        self,
        project: Any,
        report: Any,
    ) -> RepairResult:
        """
        Placeholder execution.

        Actual restoration will be delegated later
        to ProjectRepairEngine.
        """

        return RepairResult.skipped_result(
            action=self.action_type,
            message=(
                "Intelligent repair action "
                "planned but not executed."
            ),
            offset=self.offset,
            size=self.size,
            object_type=self.object_type,
            confidence=self.confidence,
        )