from __future__ import annotations

from copy import deepcopy
from typing import Any

from .integrity_report import IntegrityReport
from .repair_action import RepairAction, RepairResult


class ProjectRepairEngine:
    """
    Applies repairs to a Capture project.

    The engine never mutates the original project.
    A repaired copy is always returned.
    """

    def __init__(self) -> None:
        self._repairs: list[str] = []
        self._actions: list[RepairAction] = []
        self._results: list[RepairResult] = []

    @property
    def repairs(self) -> tuple[str, ...]:
        """
        Returns the repairs applied during the last execution.
        """
        return tuple(self._repairs)

    @property
    def actions(self) -> tuple[RepairAction, ...]:
        """
        Registered repair actions.
        """
        return tuple(self._actions)

    @property
    def results(self) -> tuple[RepairResult, ...]:
        """
        Results produced by the last repair execution.
        """
        return tuple(self._results)

    def register(
        self,
        action: RepairAction,
    ) -> None:
        """
        Register a repair action.
        """
        self._actions.append(action)
        self._actions.sort()

    def clear(self) -> None:
        """
        Clears the repair history.
        """
        self._repairs.clear()
        self._results.clear()

    def clear_actions(self) -> None:
        """
        Removes every registered repair action.
        """
        self._actions.clear()

    def repair(
        self,
        project: Any,
        report: IntegrityReport,
    ) -> Any:
        """
        Repairs a project according to an IntegrityReport.
        """

        self.clear()

        repaired = deepcopy(project)

        for action in self._actions:

            if not action.applicable(
                repaired,
                report,
            ):
                continue

            result = action.execute(
                repaired,
                report,
            )

            self._results.append(result)

            if result.executed:
                self._repairs.append(action.name)

        return repaired