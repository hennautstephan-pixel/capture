from capture_recovery.reconstruction import (
    ReconstructionPipeline,
)

from capture_recovery.formats import (
    CaptureProject,
)


def test_pipeline_validation():

    project = CaptureProject(
        name="Recovered",
    )


    result = (
        ReconstructionPipeline()
        .process(
            project,
        )
    )


    assert result["valid"]

    assert result["errors"] == []