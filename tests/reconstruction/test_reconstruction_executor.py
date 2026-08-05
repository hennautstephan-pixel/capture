from capture_recovery.reconstruction import (
    ReconstructionExecutor,
    ReconstructionDecision,
)



def test_executor_applies_replacement():

    executor = ReconstructionExecutor()


    decision = ReconstructionDecision(
        offset=2,
        size=3,
        replacement=b"XYZ",
        object_type="fixture",
        confidence=1.0,
        source="reference.c2p",
    )


    result = executor.execute(
        b"AABBBCC",
        decision,
    )


    assert result.success is True

    assert (
        result.data
        ==
        b"AAXYZCC"
    )



def test_executor_rejects_out_of_range():

    executor = ReconstructionExecutor()


    decision = ReconstructionDecision(
        offset=20,
        size=5,
        replacement=b"DATA",
        object_type="fixture",
        confidence=1.0,
        source="reference.c2p",
    )


    result = executor.execute(
        b"ABC",
        decision,
    )


    assert result.success is False

    assert result.data == b"ABC"