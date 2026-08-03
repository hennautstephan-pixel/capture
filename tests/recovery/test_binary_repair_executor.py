from capture_recovery.recovery import (
    BinaryRepairExecutor,
    IntelligentRestoreAction,
)


def test_binary_executor_applies_action(tmp_path):

    source = tmp_path / "source.c2p"

    output = tmp_path / "output.c2p"


    source.write_bytes(
        b"AAAAxxxxBBBB"
    )


    action = IntelligentRestoreAction(
        offset=4,
        size=4,
        object_type="fixture",
        confidence=0.95,
    )


    executor = BinaryRepairExecutor()


    result = executor.execute_action(
        action,
        source,
        output,
        b"YYYY",
    )


    assert output.exists()

    assert (
        output.read_bytes()
        ==
        b"AAAAYYYYBBBB"
    )


    assert (
        result.output
        ==
        output
    )



def test_binary_executor_keeps_source(tmp_path):

    source = tmp_path / "source.c2p"

    output = tmp_path / "output.c2p"


    source.write_bytes(
        b"123456"
    )


    action = IntelligentRestoreAction(
        offset=0,
        size=1,
        object_type="header",
        confidence=0.9,
    )


    executor = BinaryRepairExecutor()


    executor.execute_action(
        action,
        source,
        output,
        b"X",
    )


    assert (
        source.read_bytes()
        ==
        b"123456"
    )