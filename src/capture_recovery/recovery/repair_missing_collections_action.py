from __future__ import annotations

from typing import Any

from .repair_action import RepairAction, RepairResult


class RepairMissingCollectionsAction(RepairAction):
    """
    Ensures that common project collections are initialized.

    Missing collections are replaced by empty lists.
    """

    priority = 1000

    COLLECTIONS = (
        "fixtures",
        "groups",
        "layers",
        "universes",
        "scenes",
        "views",
        "filters",
        "palettes",
    )

    def applicable(
        self,
        project: Any,
        report: Any,
    ) -> bool:

        return True

    def execute(
        self,
        project: Any,
        report: Any,
    ) -> RepairResult:

        repaired = 0

        for name in self.COLLECTIONS:

            if not hasattr(project, name):
                continue

            if getattr(project, name) is None:
                setattr(project, name, [])
                repaired += 1

        if repaired == 0:
            return RepairResult.skipped_result(
                action=self.name,
                message="No missing collections.",
            )

        return RepairResult.success_result(
            action=self.name,
            repaired_objects=repaired,
            message=f"{repaired} collection(s) initialized.",
        )