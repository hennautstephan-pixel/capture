from __future__ import annotations

from copy import deepcopy
from typing import Any

from .integrity_report import IntegrityReport


class ObjectRepairEngine:
    """
    Repairs a single object inside a Capture project.

    The engine never mutates the original object.
    """

    def __init__(self) -> None:
        self._repairs: list[str] = []

    @property
    def repairs(self) -> tuple[str, ...]:
        return tuple(self._repairs)

    def clear(self) -> None:
        self._repairs.clear()

    def repair(
        self,
        obj: Any,
        *,
        project: Any = None,
        report: IntegrityReport | None = None,
    ) -> Any:
        """
        Repairs one object and returns a repaired copy.
        """

        self.clear()

        repaired = deepcopy(obj)

        #
        # Future commits:
        #
        # repair_guid(...)
        # repair_name(...)
        # repair_transform(...)
        # repair_parent(...)
        # repair_references(...)
        #

        return repaired