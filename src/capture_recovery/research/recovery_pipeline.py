from __future__ import annotations

from dataclasses import dataclass

from .object_mapper import ObjectMap
from .project_layout import ProjectLayout
from .repair_engine import (
    RepairEngine,
    RepairEngineResult,
)


@dataclass(slots=True, frozen=True)
class RecoveryResult:
    """
    Result of a complete recovery operation.
    """

    repair: RepairEngineResult

    output_data: bytes

    @property
    def success(self) -> bool:
        return self.repair.success

    @property
    def size(self) -> int:
        return len(self.output_data)

    @property
    def warning_count(self) -> int:
        return self.repair.warning_count

    @property
    def image(self) -> bytes:
        """
        Return the rebuilt project image.
        """
        return self.output_data

    @property
    def is_empty(self) -> bool:
        """
        Return True if no output image was produced.
        """
        return self.size == 0


class RecoveryPipeline:
    """
    Execute the complete Capture recovery pipeline.

    This class is intentionally lightweight and delegates
    all domain-specific work to the repair engine.
    """

    def __init__(self) -> None:

        self._engine = RepairEngine()

    def recover(
        self,
        layout: ProjectLayout,
        objects: ObjectMap,
        header: bytes,
        footer: bytes,
    ) -> RecoveryResult:

        repair = self._engine.repair(
            layout,
            objects,
            header,
            footer,
        )

        return RecoveryResult(
            repair=repair,
            output_data=repair.rebuild.image.data,
        )