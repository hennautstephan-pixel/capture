from capture_recovery.recovery import (
    FullRecoveryPipeline,
)

from capture_recovery.reconstruction import (
    ObjectLibrary,
)



def test_full_recovery_pipeline_creation():

    pipeline = FullRecoveryPipeline(
        object_library=ObjectLibrary(),
    )

    assert pipeline is not None