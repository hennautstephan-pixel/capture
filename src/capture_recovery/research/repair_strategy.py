from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum, auto

from .integrity_analyzer import IntegrityReport
from .knowledge_base import KnowledgeBase
from .project_layout import ProjectLayout


class RepairAction(Enum):
    """
    Possible repair actions.
    """

    NONE = auto()

    REPAIR_HEADER = auto()

    REPAIR_STREAM = auto()

    REPAIR_FOOTER = auto()

    REBUILD_PROJECT = auto()

    EXTRACT_DATA = auto()


class RepairPriority(IntEnum):
    """
    Execution priority for repair steps.
    """

    HEADER = 10
    STREAM = 20
    FOOTER = 30
    REBUILD = 100
    FALLBACK = 1000


@dataclass(slots=True, frozen=True)
class RepairStep:
    """
    One repair action.
    """

    action: RepairAction

    reason: str

    priority: RepairPriority


@dataclass(slots=True, frozen=True)
class RepairPlan:
    """
    Ordered repair plan.
    """

    steps: list[RepairStep]

    score: float

    @property
    def step_count(self) -> int:
        return len(self.steps)

    @property
    def requires_rebuild(self) -> bool:
        """
        True if the repair strategy includes a
        full project rebuild.
        """

        return any(
            step.action is RepairAction.REBUILD_PROJECT
            for step in self.steps
        )

    def ordered(self) -> list[RepairStep]:

        return sorted(
            self.steps,
            key=lambda step: step.priority,
        )


class RepairStrategy:
    """
    Build a repair strategy from the project analysis.
    """

    def build(
        self,
        integrity: IntegrityReport,
        layout: ProjectLayout,
        knowledge: KnowledgeBase,
    ) -> RepairPlan:

        steps: list[RepairStep] = []

        if integrity.error_count:

            if layout.header.length == 0:

                steps.append(
                    RepairStep(
                        RepairAction.REPAIR_HEADER,
                        "Header is missing or invalid.",
                        RepairPriority.HEADER,
                    )
                )

            if layout.stream.length == 0:

                steps.append(
                    RepairStep(
                        RepairAction.REPAIR_STREAM,
                        "Stream is missing.",
                        RepairPriority.STREAM,
                    )
                )

            if layout.footer.length == 0:

                steps.append(
                    RepairStep(
                        RepairAction.REPAIR_FOOTER,
                        "Footer is missing.",
                        RepairPriority.FOOTER,
                    )
                )

            if integrity.score < 0.50:

                steps.append(
                    RepairStep(
                        RepairAction.REBUILD_PROJECT,
                        "Project integrity is too low.",
                        RepairPriority.REBUILD,
                    )
                )

        if (
            not steps
            and knowledge.entry_count
        ):

            steps.append(
                RepairStep(
                    RepairAction.NONE,
                    "No repair required.",
                    RepairPriority.FALLBACK,
                )
            )

        if (
            not steps
            and not knowledge.entry_count
        ):

            steps.append(
                RepairStep(
                    RepairAction.EXTRACT_DATA,
                    "Project cannot be rebuilt reliably.",
                    RepairPriority.FALLBACK,
                )
            )

        return RepairPlan(
            steps=steps,
            score=integrity.score,
        )