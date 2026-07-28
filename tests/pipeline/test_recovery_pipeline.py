import json


from capture_recovery.pipeline import (
    RecoveryPipeline,
)

from capture_recovery.formats import (
    CaptureProject,
)


def test_recovery_pipeline(
    tmp_path,
):

    file = tmp_path / "capture.json"


    file.write_text(
        json.dumps(
            {
                "name": "Recovered"
            }
        ),
        encoding="utf-8",
    )


    project = CaptureProject(
        name="Recovered",
    )


    result = (
        RecoveryPipeline()
        .run(
            file,
            project,
        )
    )


    assert result["source"]["name"] == (
        "Recovered"
    )


    assert result["validation"]["valid"]

    assert result["project"] is project