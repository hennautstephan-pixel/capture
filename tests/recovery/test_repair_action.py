import pytest

from capture_recovery.recovery import (
    RepairAction,
    RepairResult,
    RepairStatus,
)


class DummyRepairAction(RepairAction):

    def execute(
        self,
        project,
        report,
    ) -> RepairResult:

        return RepairResult.success_result(
            action=self.name,
            repaired_objects=1,
            message="dummy repair",
        )


def test_action_name():

    action = DummyRepairAction()

    assert action.name == "DummyRepairAction"


def test_action_priority():

    action = DummyRepairAction()

    assert action.priority == 100


def test_action_applicable():

    action = DummyRepairAction()

    assert action.applicable(None, None)


def test_execute():

    action = DummyRepairAction()

    result = action.execute(None, None)

    assert result.succeeded
    assert result.executed
    assert result.action == "DummyRepairAction"
    assert result.repaired_objects == 1


def test_success_result():

    result = RepairResult.success_result(
        action="Repair",
        repaired_objects=2,
        message="ok",
    )

    assert result.succeeded
    assert not result.failed
    assert not result.skipped
    assert not result.blocked
    assert result.executed
    assert result.repaired_objects == 2


def test_failed_result():

    result = RepairResult.failed_result(
        action="Repair",
        message="failed",
    )

    assert result.failed
    assert not result.succeeded
    assert result.executed


def test_skipped_result():

    result = RepairResult.skipped_result(
        action="Repair",
    )

    assert result.skipped
    assert not result.executed


def test_blocked_result():

    result = RepairResult.blocked_result(
        action="Repair",
    )

    assert result.blocked
    assert not result.executed


def test_to_dict():

    result = RepairResult.success_result(
        action="Repair",
        repaired_objects=5,
        message="done",
        offset=123,
    )

    d = result.to_dict()

    assert d["status"] == "success"
    assert d["action"] == "Repair"
    assert d["message"] == "done"
    assert d["repaired_objects"] == 5
    assert d["metadata"]["offset"] == 123


def test_metadata_is_immutable():

    result = RepairResult.success_result(
        action="Repair",
        answer=42,
    )

    with pytest.raises(TypeError):
        result.metadata["answer"] = 0


def test_priority_sorting():

    class HighPriority(DummyRepairAction):
        priority = 1000

    class LowPriority(DummyRepairAction):
        priority = 10

    actions = [
        LowPriority(),
        HighPriority(),
    ]

    actions.sort()

    assert isinstance(
        actions[0],
        HighPriority,
    )


def test_repr():

    action = DummyRepairAction()

    assert (
        repr(action)
        == "DummyRepairAction(priority=100)"
    )