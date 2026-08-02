from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from .repair_strategy import (
    RepairAction,
    RepairPlan as StrategyPlan,
    RepairPriority,
)


class RepairPhase(Enum):
    """
    High-level execution phases.
    """

    PREPARE = auto()

    REBUILD = auto()

    VALIDATE = auto()

    WRITE = auto()


class RepairOperation(Enum):
    """
    Atomic repair operations.

    These operations are executable by future
    rebuild engines.
    """

    READ_HEADER = auto()

    REBUILD_HEADER = auto()

    READ_STREAM = auto()

    REBUILD_STREAM = auto()

    READ_FOOTER = auto()

    REBUILD_FOOTER = auto()

    VALIDATE = auto()

    WRITE_PROJECT = auto()


@dataclass(slots=True, frozen=True)
class RepairTask:
    """
    One executable repair task.
    """

    operation: RepairOperation

    description: str

    priority: RepairPriority

    phase: RepairPhase = RepairPhase.PREPARE


@dataclass(slots=True, frozen=True)
class ExecutionPlan:
    """
    Ordered executable repair plan.
    """

    tasks: list[RepairTask]

    @property
    def task_count(self) -> int:
        return len(self.tasks)

    def ordered(self) -> list[RepairTask]:
        """
        Return tasks ordered by priority and execution phase.
        """

        phase_order = {
            RepairPhase.PREPARE: 0,
            RepairPhase.REBUILD: 1,
            RepairPhase.WRITE: 2,
            RepairPhase.VALIDATE: 3,
        }

        return sorted(
            self.tasks,
            key=lambda task: (
                task.priority,
                phase_order[task.phase],
            ),
        )

    def by_phase(
        self,
        phase: RepairPhase,
    ) -> list[RepairTask]:

        return [
            task
            for task in self.ordered()
            if task.phase is phase
        ]

    def requires_write(self) -> bool:
        """
        Return True if the plan writes a rebuilt project.
        """

        return any(
            task.operation is RepairOperation.WRITE_PROJECT
            for task in self.tasks
        )


class RepairPlanner:
    """
    Convert a repair strategy into an executable plan.
    """

    def build(
        self,
        strategy: StrategyPlan,
    ) -> ExecutionPlan:

        tasks: list[RepairTask] = []

        for step in strategy.ordered():

            match step.action:

                case RepairAction.REPAIR_HEADER:

                    tasks.extend(
                        (
                            RepairTask(
                                RepairOperation.READ_HEADER,
                                "Read existing header.",
                                RepairPriority.HEADER,
                                RepairPhase.PREPARE,
                            ),
                            RepairTask(
                                RepairOperation.REBUILD_HEADER,
                                "Rebuild header.",
                                RepairPriority.HEADER,
                                RepairPhase.REBUILD,
                            ),
                        )
                    )

                case RepairAction.REPAIR_STREAM:

                    tasks.extend(
                        (
                            RepairTask(
                                RepairOperation.READ_STREAM,
                                "Read compressed stream.",
                                RepairPriority.STREAM,
                                RepairPhase.PREPARE,
                            ),
                            RepairTask(
                                RepairOperation.REBUILD_STREAM,
                                "Rebuild compressed stream.",
                                RepairPriority.STREAM,
                                RepairPhase.REBUILD,
                            ),
                        )
                    )

                case RepairAction.REPAIR_FOOTER:

                    tasks.extend(
                        (
                            RepairTask(
                                RepairOperation.READ_FOOTER,
                                "Read footer.",
                                RepairPriority.FOOTER,
                                RepairPhase.PREPARE,
                            ),
                            RepairTask(
                                RepairOperation.REBUILD_FOOTER,
                                "Rebuild footer.",
                                RepairPriority.FOOTER,
                                RepairPhase.REBUILD,
                            ),
                        )
                    )

                case RepairAction.REBUILD_PROJECT:

                    tasks.append(
                        RepairTask(
                            RepairOperation.WRITE_PROJECT,
                            "Write rebuilt project.",
                            RepairPriority.REBUILD,
                            RepairPhase.WRITE,
                        )
                    )

                case RepairAction.NONE:

                    tasks.append(
                        RepairTask(
                            RepairOperation.VALIDATE,
                            "Validate project.",
                            RepairPriority.FALLBACK,
                            RepairPhase.VALIDATE,
                        )
                    )

                case RepairAction.EXTRACT_DATA:

                    tasks.append(
                        RepairTask(
                            RepairOperation.READ_STREAM,
                            "Extract recoverable data.",
                            RepairPriority.FALLBACK,
                            RepairPhase.PREPARE,
                        )
                    )

        if (
            tasks
            and not any(
                task.operation is RepairOperation.VALIDATE
                for task in tasks
            )
        ):

            tasks.append(
                RepairTask(
                    RepairOperation.VALIDATE,
                    "Validate rebuilt project.",
                    RepairPriority.FALLBACK,
                    RepairPhase.VALIDATE,
                )
            )

        return ExecutionPlan(tasks)