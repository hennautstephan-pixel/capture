from capture_recovery.research import (
    RecoveryPipeline,
    RecoveryResult,
)


def test_pipeline():

    pipeline = RecoveryPipeline()

    assert isinstance(
        pipeline,
        RecoveryPipeline,
    )


def test_result():

    result = RecoveryResult(
        repair=None,
        output_data=b"",
    )

    assert result.size == 0