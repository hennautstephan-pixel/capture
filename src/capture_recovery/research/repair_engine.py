from __future__ import annotations

from dataclasses import dataclass

from .integrity_analyzer import (
    IntegrityAnalyzer,
    IntegrityReport,
)
from .object_mapper import ObjectMap
from .project_layout import ProjectLayout
from .project_rebuilder import (
    ProjectRebuilder,
    ProjectRebuildResult,
)
from .repair_plan import RepairPlanner
from .repair_strategy import RepairStrategy
from .stream_rebuilder import StreamRebuilder


@dataclass(slots=True, frozen=True)
class RepairEngineResult:
    """
    Complete repair result.
    """

    integrity: IntegrityReport

    rebuild: ProjectRebuildResult

    success: bool

    @property
    def warning_count(self) -> int:
        """
        Number of warnings generated during repair.
        """
        return self.rebuild.warning_count

    @property
    def repaired_size(self) -> int:
        """
        Size of the rebuilt project image.
        """
        return self.rebuild.image.size

    @property
    def is_empty(self) -> bool:
        """
        True if no rebuilt project was produced.
        """
        return self.rebuild.image.is_empty

    @property
    def has_warnings(self) -> bool:
        """
        Return True if warnings were generated.
        """
        return self.warning_count > 0

    @property
    def is_repaired(self) -> bool:
        """
        Alias for the repair status.
        """
        return self.success


class RepairEngine:
    """
    Complete project repair engine.

    This class orchestrates the complete repair workflow
    but delegates all domain-specific work to the
    specialized components.
    """

    def __init__(self) -> None:

        self._integrity = IntegrityAnalyzer()

        self._strategy = RepairStrategy()

        self._planner = RepairPlanner()

        self._stream = StreamRebuilder()

        self._project = ProjectRebuilder()

    def repair(
        self,
        layout: ProjectLayout,
        objects: ObjectMap,
        header: bytes,
        footer: bytes,
    ) -> RepairEngineResult:

        integrity = self._integrity.analyze(layout)

        strategy = self._strategy.build(integrity)

        plan = self._planner.build(strategy)

        stream = self._stream.rebuild(
            plan,
            objects,
        )

        rebuild = self._project.rebuild(
            plan,
            header,
            stream,
            footer,
        )

        success = (
            rebuild.is_valid
            and not rebuild.image.is_empty
        )

        return RepairEngineResult(
            integrity=integrity,
            rebuild=rebuild,
            success=success,
        )