from capture_recovery.recovery import (
    IntelligentRecoveryPipeline,
)


def test_pipeline_creation():

    pipeline = IntelligentRecoveryPipeline()

    assert pipeline is not None