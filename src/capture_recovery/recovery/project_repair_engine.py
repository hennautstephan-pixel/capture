from __future__ import annotations

from copy import deepcopy
from typing import Any

from .integrity_report import IntegrityReport


class ProjectRepairEngine:
    """
    Applies repairs to a Capture project.

    The engine never mutates the original project.
    A repaired copy is always returned.
    """

    def __init__(self) -> None:
        self._repairs: list[str] = []

    @property
    def repairs(self) -> tuple[str, ...]:
        """
        Returns the repairs applied during the last execution.
        """
        return tuple(self._repairs)

    def clear(self) -> None:
        """
        Clears the repair history.
        """
        self._repairs.clear()

    def repair(
        self,
        project: Any,
        report: IntegrityReport,
    ) -> Any:
        """
        Repairs a project according to an IntegrityReport.

        For now no repair is applied.
        A deep copy of the project is returned.
        """

        self.clear()

        repaired = deepcopy(project)

        # Future commits:
        #
        # - repair GUIDs
        # - repair references
        # - repair hierarchy
        # - repair scenes
        # - repair universes
        #

        return repaired