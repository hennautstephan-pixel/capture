from __future__ import annotations

from capture_recovery.research import (
    ExecutionPlan,
    RepairAction,
    RepairOperation,
    RepairPhase,
    RepairPlan,
    RepairPlanner,
    RepairPriority,
    RepairStep,
    RepairTask,
)


def create_plan():

    return RepairPlan(
        [
            RepairStep(
                RepairAction.REPAIR_HEADER,
                "",
                RepairPriority.HEADER,
            ),
            RepairStep(
                RepairAction.REPAIR_STREAM,
                "",
                RepairPriority.STREAM,
            ),
        ],
        1.0,
    )


def test_empty():

    planner = RepairPlanner()

    plan = planner.build(
        RepairPlan([], 1.0)
    )

    assert isinstance(
        plan,
        ExecutionPlan,
    )

    assert plan.task_count == 0


def test_header():

    planner = RepairPlanner()

    plan = planner.build(
        RepairPlan(
            [
                RepairStep(
                    RepairAction.REPAIR_HEADER,
                    "",
                    RepairPriority.HEADER,
                )
            ],
            1.0,
        )
    )

    assert plan.task_count == 3

    assert (
        plan.tasks[0].operation
        is RepairOperation.READ_HEADER
    )


def test_stream():

    planner = RepairPlanner()

    plan = planner.build(
        RepairPlan(
            [
                RepairStep(
                    RepairAction.REPAIR_STREAM,
                    "",
                    RepairPriority.STREAM,
                )
            ],
            1.0,
        )
    )

    assert any(
        task.operation
        is RepairOperation.REBUILD_STREAM
        for task in plan.tasks
    )


def test_order():

    planner = RepairPlanner()

    plan = planner.build(
        create_plan()
    )

    ordered = plan.ordered()

    assert (
        ordered[0].priority
        is RepairPriority.HEADER
    )


def test_validate():

    planner = RepairPlanner()

    plan = planner.build(
        RepairPlan(
            [
                RepairStep(
                    RepairAction.NONE,
                    "",
                    RepairPriority.FALLBACK,
                )
            ],
            1.0,
        )
    )

    assert any(
        task.operation
        is RepairOperation.VALIDATE
        for task in plan.tasks
    )


def test_task():

    task = RepairTask(
        RepairOperation.READ_HEADER,
        "",
        RepairPriority.HEADER,
        RepairPhase.PREPARE,
    )

    assert (
        task.priority
        is RepairPriority.HEADER
    )

    assert (
        task.phase
        is RepairPhase.PREPARE
    )