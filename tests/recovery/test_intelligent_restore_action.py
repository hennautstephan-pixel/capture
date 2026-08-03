from capture_recovery.recovery import (
    IntelligentRestoreAction,
)


def test_intelligent_restore_action_creation():

    action = IntelligentRestoreAction(
        offset=100,
        size=500,
        object_type="fixture",
        confidence=0.9,
    )


    assert action.offset == 100

    assert action.size == 500

    assert action.object_type == "fixture"

    assert action.confidence == 0.9



def test_intelligent_restore_action_type():

    action = IntelligentRestoreAction(
        offset=0,
        size=256,
        object_type="projector",
        confidence=0.95,
    )


    assert (
        action.action_type
        == "restore_object"
    )



def test_intelligent_restore_action_priority():

    action = IntelligentRestoreAction(
        offset=50,
        size=128,
        object_type="fixture",
        confidence=0.8,
    )


    assert (
        action.priority
        == 100
    )



def test_intelligent_restore_action_execute():

    action = IntelligentRestoreAction(
        offset=200,
        size=1024,
        object_type="fixture",
        confidence=0.85,
    )


    result = action.execute(
        project=None,
        report=None,
    )


    assert result is not None

    assert (
        result.action
        == "restore_object"
    )

    assert (
        "planned"
        in result.message
    )