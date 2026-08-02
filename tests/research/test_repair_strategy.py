from __future__ import annotations

from capture_recovery.research import (
    IntegrityReport,
    KnowledgeBase,
    KnowledgeEntry,
    ObjectMap,
    ProjectLayoutBuilder,
    RepairAction,
    RepairPlan,
    RepairPriority,
    RepairStep,
    RepairStrategy,
)


def create_layout():

    return ProjectLayoutBuilder().build(
        file_size=100,
        header_size=10,
        stream_offset=10,
        stream_length=80,
        footer_size=10,
        objects=ObjectMap([]),
    )


def test_empty():

    strategy = RepairStrategy()

    plan = strategy.build(
        IntegrityReport([], 1.0),
        create_layout(),
        KnowledgeBase(),
    )

    assert isinstance(
        plan,
        RepairPlan,
    )


def test_no_repair():

    strategy = RepairStrategy()

    kb = KnowledgeBase()

    kb.add(
        KnowledgeEntry(
            offset=0,
            length=4,
            type_candidates=("bytes",),
            confidence=1.0,
            evidence=("test",),
        )
    )

    plan = strategy.build(
        IntegrityReport([], 1.0),
        create_layout(),
        kb,
    )

    assert plan.step_count == 1

    assert (
        plan.steps[0].action
        is RepairAction.NONE
    )


def test_extract():

    strategy = RepairStrategy()

    plan = strategy.build(
        IntegrityReport([], 1.0),
        create_layout(),
        KnowledgeBase(),
    )

    assert plan.step_count == 1

    assert (
        plan.steps[0].action
        is RepairAction.EXTRACT_DATA
    )


def test_order():

    plan = RepairPlan(
        [
            RepairStep(
                RepairAction.REPAIR_STREAM,
                "",
                RepairPriority.STREAM,
            ),
            RepairStep(
                RepairAction.REPAIR_HEADER,
                "",
                RepairPriority.HEADER,
            ),
        ],
        1.0,
    )

    ordered = plan.ordered()

    assert (
        ordered[0].priority
        is RepairPriority.HEADER
    )


def test_step_count():

    plan = RepairPlan(
        [],
        1.0,
    )

    assert plan.step_count == 0